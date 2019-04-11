// XMediaSplitter.cpp BOF####################################################################################BOF
#include "StdAfx.h"
#include "GUIDs.h"                      // CLSID_RMSplitter
#include "XMediaFormat.h"               // rvinfo, rainfo, rainfo4, rainfo5
                                        // WAVE_FORMAT_14_4 ... and MEDIASUBTYPE_WAVE_DOLBY_AC3 ...
#include "BaseSplitter.h"               // CBaseSplitter, CBaseSplitterOutputPin, Paket
#include "BaseSplitterFile.h"           // cBaseSplitterFile
#include "DSUtil.h"                     // MakeAACInitData

#include "XMediaSplitter.h"     // namespace RMFF, CXMediaSplitter

template<typename Type> static void bswap(Type& var)
{
    BYTE* s = (BYTE*) &var;
    BYTE* d = s + sizeof(var) - 1;
    while (s < d)
    {
        *s ^= *d;
        *d ^= *s;
        *s ^= *d;
        s++;
        d--;
    }     
}

void rvinfo::bswap()
{
    ::bswap(dwSize);
    ::bswap(w); ::bswap(h); ::bswap(bpp);
    ::bswap(unk1); ::bswap(fps); 
    ::bswap(type1); ::bswap(type2);
}

void rainfo::bswap()
{
    ::bswap(version1);
    ::bswap(version2);
    ::bswap(header_size);
    ::bswap(flavor);
    ::bswap(packetSize);
    ::bswap(maxPackets);
    ::bswap(frame_size);
    ::bswap(subPacketSize);
}

void rainfo4::bswap()
{
    __super::bswap();
    ::bswap(sample_rate);
    ::bswap(sample_size);
    ::bswap(channels);
}

void rainfo5::bswap()
{
    __super::bswap();
    ::bswap(sample_rate);
    ::bswap(sample_size);
    ::bswap(channels);
}

class CXMediaSplitterOutputPin : public CBaseSplitterOutputPin
{
public:
    CXMediaSplitterOutputPin(
        CArray<CMediaType>& mts, LPCWSTR pName, CBaseFilter* pFilter, CCritSec* pLock, HRESULT* phr);
    virtual ~CXMediaSplitterOutputPin();

    HRESULT DeliverEndFlush();

protected:
    HRESULT DeliverPacket(CAutoPtr<Packet> p);

private:
    typedef struct {CArray<BYTE> data; DWORD offset;} segment;

    class CSegments : public CAutoPtrList<segment>, public CCritSec
    {
    public:
        REFERENCE_TIME rtStart; 
        bool fDiscontinuity, fSyncPoint, fMerged;
        void Clear()
        {
            CAutoLock cAutoLock(this);
            rtStart = 0;
            fDiscontinuity = fSyncPoint = fMerged = false;
            RemoveAll();
        }
    } m_segments;

    CCritSec m_csQueue;

    HRESULT DeliverSegments();
};

//
// CXMediaSplitterFilter
//
using namespace RMFF;

CXMediaSplitterFilter::CXMediaSplitterFilter(LPUNKNOWN pUnk, HRESULT* phr)
: CBaseSplitterFilter(NAME("CXMediaSplitterFilter"), pUnk, phr, CLSID_RMSplitter)
{
}

CXMediaSplitterFilter::~CXMediaSplitterFilter()
{
}

HRESULT CXMediaSplitterFilter::CreateOutputs(IAsyncReader* pAsyncReader)
{
    CheckPointer(pAsyncReader, E_POINTER);

    {
        DWORD dw;
        if(FAILED(pAsyncReader->SyncRead(0, 4, (BYTE*)&dw)) || dw != 'FMR.')
            return E_FAIL;
    }

    HRESULT hr = E_FAIL;

    m_pFile.Free();
    m_pChapters.RemoveAll();

    m_pFile.Attach(new CRMFile(pAsyncReader, hr));
    if(!m_pFile) return E_OUTOFMEMORY;
    if(FAILED(hr)) {m_pFile.Free(); return hr;}

    m_rtNewStart = m_rtCurrent = 0;
    m_rtNewStop = m_rtStop = 0;

    m_rtStop = 10000i64*m_pFile->m_p.tDuration;

    POSITION pos = m_pFile->m_mps.GetHeadPosition();
    while(pos)
    {
        MediaProperies* pmp = m_pFile->m_mps.GetNext(pos);

        CStringW name;
        name.Format(L"Output %d", pmp->stream);
        if(!pmp->name.IsEmpty()) name += L" (" + CStringW(pmp->name) + L")";

        CArray<CMediaType> mts;

        CMediaType mt;
        mt.SetSampleSize(max(pmp->maxPacketSize*16, 1));

        if(pmp->mime == "video/x-pn-Xvideo")
        {
            mt.majortype = MEDIATYPE_Video;
            mt.formattype = FORMAT_VideoInfo;

            VIDEOINFOHEADER* pvih =
                (VIDEOINFOHEADER*) mt.AllocFormatBuffer(sizeof(VIDEOINFOHEADER) + pmp->typeSpecData.GetCount());
            memset(mt.Format(), 0, mt.FormatLength());
            memcpy(pvih + 1, pmp->typeSpecData.GetData(), pmp->typeSpecData.GetCount());

            rvinfo rvi = *(rvinfo*)pmp->typeSpecData.GetData();
            rvi.bswap();

            ASSERT(rvi.dwSize >= FIELD_OFFSET(rvinfo, morewh));
            ASSERT(rvi.fcc1 == 'ODIV');

            mt.subtype = FOURCCMap(rvi.fcc2);
            if(rvi.fps > 0x10000) pvih->AvgTimePerFrame = REFERENCE_TIME(10000000i64 / ((float)rvi.fps/0x10000)); 
            pvih->dwBitRate = pmp->avgBitRate; 
            pvih->bmiHeader.biSize = sizeof(pvih->bmiHeader);
            pvih->bmiHeader.biWidth = rvi.w;
            pvih->bmiHeader.biHeight = rvi.h;
            pvih->bmiHeader.biPlanes = 3;
            pvih->bmiHeader.biBitCount = rvi.bpp;
            pvih->bmiHeader.biCompression = rvi.fcc2;
            pvih->bmiHeader.biSizeImage = rvi.w*rvi.h*3/2;

            mts.Add(mt);

            if(pmp->width > 0 && pmp->height > 0)
            {
                BITMAPINFOHEADER bmi = pvih->bmiHeader;
                mt.formattype = FORMAT_VideoInfo2;
                VIDEOINFOHEADER2* pvih2 =
                    (VIDEOINFOHEADER2*)mt.XlocFormatBuffer(sizeof(VIDEOINFOHEADER2) + pmp->typeSpecData.GetCount());
                memset(mt.Format() + FIELD_OFFSET(VIDEOINFOHEADER2, dwInterlaceFlags), 0,
                    mt.FormatLength() - FIELD_OFFSET(VIDEOINFOHEADER2, dwInterlaceFlags));
                memcpy(pvih2 + 1, pmp->typeSpecData.GetData(), pmp->typeSpecData.GetCount());
                pvih2->bmiHeader = bmi;
                pvih2->bmiHeader.biWidth = (DWORD)pmp->width;
                pvih2->bmiHeader.biHeight = (DWORD)pmp->height;
                pvih2->dwPictAspectRatioX = bmi.biWidth;
                pvih2->dwPictAspectRatioY = bmi.biHeight;
                mts.InsertAt(0, mt);
            }
        }
        else if(pmp->mime == "audio/x-pn-Xaudio")
        {
            mt.majortype = MEDIATYPE_Audio;
            mt.formattype = FORMAT_WaveFormatEx;

            WAVEFORMATEX* pwfe =
                (WAVEFORMATEX*) mt.AllocFormatBuffer(sizeof(WAVEFORMATEX) + pmp->typeSpecData.GetCount());
            memset(mt.Format(), 0, mt.FormatLength());
            memcpy(pwfe + 1, pmp->typeSpecData.GetData(), pmp->typeSpecData.GetCount());

            union {
                DWORD fcc;
                char fccstr[5];
            };

            fcc = 0;
            fccstr[4] = 0;

            BYTE* fmt = pmp->typeSpecData.GetData();
            for(int i = 0; i < pmp->typeSpecData.GetSize()-4; i++, fmt++)
            {
                if(fmt[0] == '.' || fmt[1] == 'r' || fmt[2] == 'a')
                    break;
            }

            rainfo rai = *(rainfo*)fmt;
            rai.bswap();

            BYTE* extra = NULL;

            if(rai.version2 == 4)
            {
                rainfo4 rai4 = *(rainfo4*)fmt;
                rai4.bswap();
                pwfe->nChannels = rai4.channels;
                pwfe->wBitsPerSample = rai4.sample_size;
                pwfe->nSamplesPerSec = rai4.sample_rate;
                pwfe->nBlockAlign = rai4.frame_size;
                BYTE* p = (BYTE*)((rainfo4*)fmt+1);
                int len = *p++; p += len; len = *p++; ASSERT(len == 4);
                if(len == 4)
                    fcc = MAKEFOURCC(p[0],p[1],p[2],p[3]);
                extra = p + len + 3;
            }
            else if(rai.version2 == 5)
            {
                rainfo5 rai5 = *(rainfo5*)fmt;
                rai5.bswap();
                pwfe->nChannels = rai5.channels;
                pwfe->wBitsPerSample = rai5.sample_size;
                pwfe->nSamplesPerSec = rai5.sample_rate;
                pwfe->nBlockAlign = rai5.frame_size;
                fcc = rai5.fourcc3;
                extra = fmt + sizeof(rainfo5) + 4;
            }
            else
            {
                continue;
            }

            _strupr(fccstr);

            mt.subtype = FOURCCMap(fcc);

            bswap(fcc);

            switch(fcc)
            {
            case 'ATRC': pwfe->wFormatTag = WAVE_FORMAT_ATRC; break;
            case 'COOK': pwfe->wFormatTag = WAVE_FORMAT_COOK; break;
            case 'SIPR': pwfe->wFormatTag = WAVE_FORMAT_SIPR; break;
            case 'RAAC': pwfe->wFormatTag = WAVE_FORMAT_RAAC; break;
            }

            if(pwfe->wFormatTag)
            {
                mts.Add(mt);
            }
        }
        else if(pmp->mime == "logical-fileinfo")
        {
            CMap<CStringA,LPCSTR,CStringA,LPCSTR> lfi;
            CStringA key, value;

            BYTE* p = pmp->typeSpecData.GetData();
            BYTE* end = p + pmp->typeSpecData.GetCount();
            p += 8;

            DWORD cnt = p <= end-4 ? *(DWORD*)p : 0; bswap(cnt); p += 4;

            if(cnt > 0xffff) // different format?
            {
                p += 2;
                cnt = p <= end-4 ? *(DWORD*)p : 0; bswap(cnt); p += 4;
            }

            while(p < end-4 && cnt-- > 0)
            {
                BYTE* base = p;
                DWORD len = *(DWORD*)p; bswap(len); p += 4;
                if(base + len > end) break;

                p++;
                WORD keylen = *(WORD*)p; bswap(keylen); p += 2;
                memcpy(key.GetBufferSetLength(keylen), p, keylen);
                p += keylen;

                p+=4;
                WORD valuelen = *(WORD*)p; bswap(valuelen); p += 2;
                memcpy(value.GetBufferSetLength(valuelen), p, valuelen);
                p += valuelen;

                ASSERT(p == base + len);
                p = base + len;

                lfi[key] = value;
            }

            POSITION pos = lfi.GetStartPosition();
            while(pos)
            {
                lfi.GetNextAssoc(pos, key, value);

                int n = strtol(key.Mid(7), NULL, 10);
                if (key.Find("CHAPTER") == 0 && key.Find("TIME") == key.GetLength() - 4 && n > 0)
                {
                    int h, m, s, ms;
                    char c;
                    if(7 != sscanf(value, "%d%c%d%c%d%c%d", &h, &c, &m, &c, &s, &c, &ms))
                        continue;

                    key.Format("CHAPTER%02dNAME", n);
                    if(!lfi.Lookup(key, value) || value.IsEmpty())
                        value.Format("Chapter %d", n);

                    CAutoPtr<CChapter> p(new CChapter(
                        ((((REFERENCE_TIME)h*60+m)*60+s)*1000+ms)*10000, 
                        CStringW(CString(value))));

                    POSITION insertpos = m_pChapters.GetTailPosition();
                    for(; insertpos; m_pChapters.GetPrev(insertpos))
                    {
                        CChapter* p2 = m_pChapters.GetAt(insertpos);
                        if(p->m_rt >= p2->m_rt) break;
                    }
                    m_pChapters.InsertAfter(insertpos, p);
                }
            }
        }

        if(mts.IsEmpty())
        {
            TRACE(_T("Unsupported XMedia stream (%d): %s\n"), pmp->stream, CString(pmp->mime));
            continue;
        }

        HRESULT hr;

        CAutoPtr<CBaseSplitterOutputPin> pPinOut(new CXMediaSplitterOutputPin(mts, name, this, this, &hr));
        if(SUCCEEDED(AddOutputPin((DWORD)pmp->stream, pPinOut)))
        {
            if(!m_rtStop)
                m_pFile->m_p.tDuration = max(m_pFile->m_p.tDuration, pmp->tDuration);
        }
    }

    pos = m_pFile->m_subs.GetHeadPosition();
    for(DWORD stream = 0; pos; stream++)
    {
        CRMFile::subtitle& s = m_pFile->m_subs.GetNext(pos);

        CStringW name;
        name.Format(L"Subtitle %02d", stream);
        if(!s.name.IsEmpty()) name += L" (" + CStringW(CString(s.name)) + L")";

        CMediaType mt;
        mt.SetSampleSize(1);
        mt.majortype = MEDIATYPE_Text;

        CArray<CMediaType> mts;
        mts.Add(mt);

        HRESULT hr;

        CAutoPtr<CBaseSplitterOutputPin> pPinOut(new CXMediaSplitterOutputPin(mts, name, this, this, &hr));
        AddOutputPin((DWORD)~stream, pPinOut);
    }

    m_rtDuration = m_rtNewStop = m_rtStop = 10000i64*m_pFile->m_p.tDuration;

    return m_pOutputs.GetCount() > 0 ? S_OK : E_FAIL;
}

bool CXMediaSplitterFilter::InitDeliverLoop()
{
    if (!m_pFile)
    {
        return false;
    }

    // reindex if needed

    if(m_pFile->m_irs.GetCount() == 0)
    {
        m_nOpenProgress = 0;
        m_rtDuration = 0;

        int stream = m_pFile->GetMasterStream();

        UINT32 tLastStart = 0xFFFFFFFF;
        UINT32 nPacket = 0;

        POSITION pos = m_pFile->m_dcs.GetHeadPosition(); 
        while(pos && !m_fAbort)
        {
            DataChunk* pdc = m_pFile->m_dcs.GetNext(pos);

            m_pFile->Seek(pdc->pos);

            for (UINT32 i = 0; i < pdc->nPackets && !m_fAbort; i++, nPacket++)
            {
                UINT64 filepos = m_pFile->GetPos();

                HRESULT hr;

                MediaPacketHeader mph;
                if(S_OK != (hr = m_pFile->Read(mph, false)))
                    break;

                if(mph.stream == stream && (mph.flags&MediaPacketHeader::PN_KEYFRAME_FLAG) && tLastStart != mph.tStart)
                {
                    m_rtDuration = max((__int64)(10000i64*mph.tStart), m_rtDuration);

                    CAutoPtr<IndexRecord> pir(new IndexRecord());
                    pir->tStart = mph.tStart;
                    pir->ptrFilePos = (UINT32) filepos;
                    pir->packet = nPacket;
                    m_pFile->m_irs.AddTail(pir);

                    tLastStart = mph.tStart;
                }

                m_nOpenProgress = m_pFile->GetPos() * 100 / m_pFile->GetLength();

                DWORD cmd;
                if (CheckRequest(&cmd))
                {
                    if (cmd == CMD_EXIT) m_fAbort = true;
                    else Reply(S_OK);
                }
            }
        }

        m_nOpenProgress = 100;

        if(m_fAbort) m_pFile->m_irs.RemoveAll();

        m_fAbort = false;
    }

    m_seekpos = NULL;
    m_seekpacket = 0;
    m_seekfilepos = 0;

    return true;
}

void CXMediaSplitterFilter::SeekDeliverLoop(REFERENCE_TIME rt)
{
    if(rt <= 0)
    {
        m_seekpos = m_pFile->m_dcs.GetHeadPosition(); 
        m_seekpacket = 0;
        m_seekfilepos = m_pFile->m_dcs.GetHead()->pos;
    }
    else
    {
        m_seekpos = NULL; 

        POSITION pos = m_pFile->m_irs.GetTailPosition();
        while(pos && !m_seekpos)
        {
            IndexRecord* pir = m_pFile->m_irs.GetPrev(pos);
            if(pir->tStart <= rt/10000)
            {
                m_seekpacket = pir->packet;

                pos = m_pFile->m_dcs.GetTailPosition();
                while(pos && !m_seekpos)
                {
                    POSITION tmp = pos;

                    DataChunk* pdc = m_pFile->m_dcs.GetPrev(pos);

                    if(pdc->pos <= pir->ptrFilePos)
                    {
                        m_seekpos = tmp;
                        m_seekfilepos = pir->ptrFilePos;

                        POSITION pos = m_pFile->m_dcs.GetHeadPosition();
                        while(pos != m_seekpos)
                        {
                            m_seekpacket -= m_pFile->m_dcs.GetNext(pos)->nPackets;
                        }
                    }
                }
            }
        }

        if(!m_seekpos)
        {
            m_seekpos = m_pFile->m_dcs.GetHeadPosition(); 
            m_seekpacket = 0;
            m_seekfilepos = m_pFile->m_dcs.GetAt(m_seekpos)->pos;
        }
    }
}

bool CXMediaSplitterFilter::DoDeliverLoop()
{
    HRESULT hr = S_OK;
    POSITION pos;

    pos = m_pFile->m_subs.GetHeadPosition();
    for(DWORD stream = 0; pos && SUCCEEDED(hr) && !CheckRequest(NULL); stream++)
    {
        CRMFile::subtitle& s = m_pFile->m_subs.GetNext(pos);

        CAutoPtr<Packet> p(new Packet);

        p->TrackNumber = ~stream;
        p->bSyncPoint = TRUE;
        p->rtStart = 0;
        p->rtStop = 1;

        int size = (4+1) + (2+4+(s.name.GetLength()+1)*2) + (2+4+s.data.GetLength());

        p->pData.SetSize(size);
        BYTE* ptr = p->pData.GetData();

        StringCchCopyA((char*)ptr, size, "GAB2"); ptr += 4+1;
        *(WORD*)ptr = 2; ptr += 2;
        *(DWORD*)ptr = (s.name.GetLength()+1)*2; ptr += 4;
        StringCchCopyW((WCHAR*)ptr, size, CStringW(s.name)); ptr += (s.name.GetLength()+1)*2;
        *(WORD*)ptr = 4; ptr += 2;
        *(DWORD*)ptr = s.data.GetLength(); ptr += 4;
        memcpy((char*)ptr, s.data, s.data.GetLength()); ptr += s.name.GetLength();

        hr = DeliverPacket(p);
    }

    pos = m_seekpos; 
    while(pos && SUCCEEDED(hr) && !CheckRequest(NULL))
    {
        DataChunk* pdc = m_pFile->m_dcs.GetNext(pos);

        m_pFile->Seek(m_seekfilepos > 0 ? m_seekfilepos : pdc->pos);

        for(UINT32 i = m_seekpacket; i < pdc->nPackets && SUCCEEDED(hr) && !CheckRequest(NULL); i++)
        {
            MediaPacketHeader mph;
            if(S_OK != (hr = m_pFile->Read(mph)))
                break;

            CAutoPtr<Packet> p(new Packet);
            p->TrackNumber = mph.stream;
            p->bSyncPoint = !!(mph.flags&MediaPacketHeader::PN_KEYFRAME_FLAG);
            p->rtStart = 10000i64*(mph.tStart);
            p->rtStop = p->rtStart+1;
            p->pData.Copy(mph.pData);
            hr = DeliverPacket(p);
        }

        m_seekpacket = 0;
        m_seekfilepos = 0;
    }

    return(true);
}

//
// CXMediaSplitterOutputPin
//

CXMediaSplitterOutputPin::CXMediaSplitterOutputPin(
    CArray<CMediaType>& mts, LPCWSTR pName, CBaseFilter* pFilter, CCritSec* pLock, HRESULT* phr)
: CBaseSplitterOutputPin(mts, pName, pFilter, pLock, phr)
{
}

CXMediaSplitterOutputPin::~CXMediaSplitterOutputPin()
{
}

HRESULT CXMediaSplitterOutputPin::DeliverEndFlush()
{
    {
        CAutoLock cAutoLock(&m_csQueue);
        m_segments.Clear();
    }

    return __super::DeliverEndFlush();
}

HRESULT CXMediaSplitterOutputPin::DeliverSegments()
{
    HRESULT hr;

    if(m_segments.GetCount() == 0)
    {
        m_segments.Clear();
        return S_OK;
    }

    CAutoPtr<Packet> p(new Packet());

    p->TrackNumber = 0xFFFFFFFF;
    p->bDiscontinuity = m_segments.fDiscontinuity;
    p->bSyncPoint = m_segments.fSyncPoint;
    p->rtStart = m_segments.rtStart;
    p->rtStop = m_segments.rtStart+1;

    DWORD len = 0, total = 0;
    POSITION pos = m_segments.GetHeadPosition();
    while(pos)
    {
        segment* s = m_segments.GetNext(pos);
        len = max(len, s->offset + s->data.GetCount());
        total += s->data.GetCount();
    }
    ASSERT(len == total); // ??????? Sometimes it happends
    len += 1 + 2*4*(!m_segments.fMerged ? m_segments.GetCount() : 1);

    p->pData.SetSize(len);

    BYTE* pData = p->pData.GetData();

    *pData++ = m_segments.fMerged ? 0 : (BYTE) (m_segments.GetCount() - 1);

    if (m_segments.fMerged)
    {
        *((DWORD*)pData) = 1; pData += 4;
        *((DWORD*)pData) = 0; pData += 4;
    }
    else
    {
        pos = m_segments.GetHeadPosition();
        while(pos)
        {
            *((DWORD*)pData) = 1; pData += 4;
            *((DWORD*)pData) = m_segments.GetNext(pos)->offset; pData += 4;
        }
    }

    pos = m_segments.GetHeadPosition();
    while(pos)
    {
        segment* s = m_segments.GetNext(pos);
        memcpy(pData + s->offset, s->data.GetData(), s->data.GetCount());
    }

    hr = __super::DeliverPacket(p);

    m_segments.Clear();

    return hr;
}

HRESULT CXMediaSplitterOutputPin::DeliverPacket(CAutoPtr<Packet> p)
{
    HRESULT hr = S_OK;

    ASSERT(p->rtStart < p->rtStop);

    if (m_mt.subtype == MEDIASUBTYPE_RV20 || m_mt.subtype == MEDIASUBTYPE_RV30 || m_mt.subtype == MEDIASUBTYPE_RV40)

    {
        CAutoLock cAutoLock(&m_csQueue);

        int len = p->pData.GetCount();
        BYTE* pIn = p->pData.GetData();
        BYTE* pInOrg = pIn;

        if(m_segments.rtStart != p->rtStart)
        {
            if(S_OK != (hr = DeliverSegments()))
                return hr;
        }

        if(!m_segments.fDiscontinuity && p->bDiscontinuity)
            m_segments.fDiscontinuity = true;
        m_segments.fSyncPoint = !!p->bSyncPoint;
        m_segments.rtStart = p->rtStart;

        while(pIn - pInOrg < len)
        {
            BYTE hdr = *pIn++, subseq = 0, seqnum = 0;
            DWORD packetlen = 0, packetoffset = 0;

            if((hdr&0xc0) == 0x40)
            {
                pIn++;
                packetlen = len - (pIn - pInOrg);
            }
            else
            {
                if((hdr&0x40) == 0)
                    subseq = (*pIn++)&0x7f;

#define GetWORD(var) \
    var = (var<<8)|(*pIn++); \
    var = (var<<8)|(*pIn++); \

                GetWORD(packetlen);
                if(packetlen&0x8000) m_segments.fMerged = true;
                if((packetlen&0x4000) == 0) {GetWORD(packetlen); packetlen &= 0x3fffffff;}
                else packetlen &= 0x3fff;

                GetWORD(packetoffset);
                if((packetoffset&0x4000) == 0) {GetWORD(packetoffset); packetoffset &= 0x3fffffff;}
                else packetoffset &= 0x3fff;

#undef GetWORD

                if((hdr&0xc0) == 0xc0)
                    m_segments.rtStart = 10000i64*packetoffset - m_rtStart, packetoffset = 0;
                else if((hdr&0xc0) == 0x80)
                    packetoffset = packetlen - packetoffset;

                seqnum = *pIn++;
            }

            int len2 = min(len - (int) (pIn - pInOrg), (int) (packetlen - packetoffset));

            CAutoPtr<segment> s(new segment);
            s->offset = packetoffset;
            s->data.SetSize(len2);
            memcpy(s->data.GetData(), pIn, len2);
            m_segments.AddTail(s);

            pIn += len2;

            if((hdr&0x80) || packetoffset+len2 >= packetlen)
            {
                if(S_OK != (hr = DeliverSegments()))
                    return hr;
            }
        }
    }
    else if (m_mt.subtype == MEDIASUBTYPE_RAAC)
    {
        BYTE* ptr = p->pData.GetData()+2;

        CList<WORD> sizes;
        int total = 0;
        int remaining = p->pData.GetSize()-2;
        int expected = *(ptr-1)>>4;

        while(total < remaining)
        {
            WORD size = (ptr[0] << 8) | (ptr[1]);
            sizes.AddTail(size);
            total += size;
            ptr += 2;
            remaining -= 2;
            expected--;
        }

        ASSERT(total == remaining);
        ASSERT(expected == 0);

        WAVEFORMATEX* wfe = (WAVEFORMATEX*)m_mt.pbFormat;
        REFERENCE_TIME rtDur = 10240000000i64/wfe->nSamplesPerSec * (wfe->cbSize>2?2:1);
        REFERENCE_TIME rtStart = p->rtStart;
        BOOL bDiscontinuity = p->bDiscontinuity;

        POSITION pos = sizes.GetHeadPosition();
        while(pos)
        {
            CAutoPtr<Packet> p(new Packet);
            p->bDiscontinuity = bDiscontinuity;
            p->bSyncPoint = true;
            p->rtStart = rtStart;
            p->rtStop = rtStart + rtDur;
            p->pData.SetSize(sizes.GetNext(pos));
            memcpy(p->pData.GetData(), ptr, p->pData.GetSize());
            ptr += p->pData.GetSize();
            rtStart = p->rtStop;
            bDiscontinuity = false;
            if(S_OK != (hr = __super::DeliverPacket(p)))
                break;
        }
    }
    else
    {
        hr = __super::DeliverPacket(p);
    }

    return hr;
}

//
// CRMFile
//

CRMFile::CRMFile(IAsyncReader* pAsyncReader, HRESULT& hr)
: CBaseSplitterFile(pAsyncReader, hr)
{
    if(FAILED(hr)) return;
    hr = Init();
}

template<typename T> 
HRESULT CRMFile::Read(T& var)
{
    HRESULT hr = Read((BYTE*)&var, sizeof(var));
    bswap(var);
    return hr;
}

HRESULT CRMFile::Read(ChunkHdr& hdr)
{
    memset(&hdr, 0, sizeof(hdr));
    HRESULT hr;
    if(S_OK != (hr = Read(hdr.object_id))
        || S_OK != (hr = Read(hdr.size))
        || S_OK != (hr = Read(hdr.object_version)))
        return hr;
    return S_OK;
}

HRESULT CRMFile::Read(MediaPacketHeader& mph, bool fFull)
{
    memset(&mph, 0, FIELD_OFFSET(MediaPacketHeader, pData));
    mph.stream = 0xFFFF;

    HRESULT hr;

    UINT16 object_version;
    if(S_OK != (hr = Read(object_version))) return hr;
    if(object_version != 0 && object_version != 1) return S_OK;

    UINT8 flags;
    if(S_OK != (hr = Read(mph.len))
        || S_OK != (hr = Read(mph.stream))
        || S_OK != (hr = Read(mph.tStart))
        || S_OK != (hr = Read(mph.reserved))
        || S_OK != (hr = Read(flags)))
        return hr;
    mph.flags = (MediaPacketHeader::flag_t)flags;

    LONG len = mph.len;
    len -= sizeof(object_version);
    len -= FIELD_OFFSET(MediaPacketHeader, flags);
    len -= sizeof(flags);
    ASSERT(len >= 0);
    len = max(len, 0);

    if(fFull)
    {
        mph.pData.SetSize(len);
        if(mph.len > 0 && S_OK != (hr = Read(mph.pData.GetData(), len)))
            return hr;
    }
    else
    {
        Seek(GetPos() + len);
    }

    return S_OK;
}


HRESULT CRMFile::Init()
{
    Seek(0);

    bool fFirstChunk = true;

    HRESULT hr;

    ChunkHdr hdr;
    while(GetPos() < GetLength() && S_OK == (hr = Read(hdr)))
    {
        __int64 pos = GetPos() - sizeof(hdr);

        if(fFirstChunk && hdr.object_id != '.RMF')
            return E_FAIL;

        fFirstChunk = false;

        if(pos + hdr.size > GetLength() && hdr.object_id != 'DATA') // truncated?
            break;

        if(hdr.object_id == 0x2E7261FD) // '.ra+0xFD'
            return E_FAIL;

        if(hdr.object_version == 0)
        {
            switch(hdr.object_id)
            {
            case '.RMF':
                if(S_OK != (hr = Read(m_fh.version))) return hr;
                if(hdr.size == 0x10) {WORD w = 0; if(S_OK != (hr = Read(w))) return hr; m_fh.nHeaders = w;}
                else if(S_OK != (hr = Read(m_fh.nHeaders))) return hr;
                break;
            case 'CONT':
                UINT16 slen;
                if(S_OK != (hr = Read(slen))) return hr;
                if(slen > 0 && S_OK != (hr = Read((BYTE*)m_cd.title.GetBufferSetLength(slen), slen))) return hr;
                if(S_OK != (hr = Read(slen))) return hr;
                if(slen > 0 && S_OK != (hr = Read((BYTE*)m_cd.author.GetBufferSetLength(slen), slen))) return hr;
                if(S_OK != (hr = Read(slen))) return hr;
                if(slen > 0 && S_OK != (hr = Read((BYTE*)m_cd.copyright.GetBufferSetLength(slen), slen))) return hr;
                if(S_OK != (hr = Read(slen))) return hr;
                if(slen > 0 && S_OK != (hr = Read((BYTE*)m_cd.comment.GetBufferSetLength(slen), slen))) return hr;
                break;
            case 'PROP':
                if(S_OK != (hr = Read(m_p.maxBitRate))) return hr;
                if(S_OK != (hr = Read(m_p.avgBitRate))) return hr;
                if(S_OK != (hr = Read(m_p.maxPacketSize))) return hr;
                if(S_OK != (hr = Read(m_p.avgPacketSize))) return hr;
                if(S_OK != (hr = Read(m_p.nPackets))) return hr;
                if(S_OK != (hr = Read(m_p.tDuration))) return hr;
                if(S_OK != (hr = Read(m_p.tPreroll))) return hr;
                if(S_OK != (hr = Read(m_p.ptrIndex))) return hr;
                if(S_OK != (hr = Read(m_p.ptrData))) return hr;
                if(S_OK != (hr = Read(m_p.nStreams))) return hr;
                UINT16 flags;
                if(S_OK != (hr = Read(flags))) return hr;
                m_p.flags = (Properies::flags_t)flags;
                break;
            case 'MDPR':
                {
                    CAutoPtr<MediaProperies> mp(new MediaProperies);
                    if(S_OK != (hr = Read(mp->stream))) return hr;
                    if(S_OK != (hr = Read(mp->maxBitRate))) return hr;
                    if(S_OK != (hr = Read(mp->avgBitRate))) return hr;
                    if(S_OK != (hr = Read(mp->maxPacketSize))) return hr;
                    if(S_OK != (hr = Read(mp->avgPacketSize))) return hr;
                    if(S_OK != (hr = Read(mp->tStart))) return hr;
                    if(S_OK != (hr = Read(mp->tPreroll))) return hr;
                    if(S_OK != (hr = Read(mp->tDuration))) return hr;
                    UINT8 slen;
                    if(S_OK != (hr = Read(slen))) return hr;
                    if(slen > 0 && S_OK != (hr = Read((BYTE*)mp->name.GetBufferSetLength(slen), slen))) return hr;
                    if(S_OK != (hr = Read(slen))) return hr;
                    if(slen > 0 && S_OK != (hr = Read((BYTE*)mp->mime.GetBufferSetLength(slen), slen))) return hr;
                    UINT32 tsdlen;
                    if(S_OK != (hr = Read(tsdlen))) return hr;
                    mp->typeSpecData.SetSize(tsdlen);
                    if(tsdlen > 0 && S_OK != (hr = Read(mp->typeSpecData.GetData(), tsdlen))) return hr;
                    mp->width = mp->height = 0;
                    m_mps.AddTail(mp);
                    break;
                }
            case 'DATA':
                {
                    CAutoPtr<DataChunk> dc(new DataChunk);
                    if(S_OK != (hr = Read(dc->nPackets))) return hr;
                    if(S_OK != (hr = Read(dc->ptrNext))) return hr;
                    dc->pos = GetPos();
                    m_dcs.AddTail(dc);
                    GetDimensions();
                    break;
                }
            case 'INDX':
                {
                    IndexChunkHeader ich;
                    if(S_OK != (hr = Read(ich.nIndices))) return hr;
                    if(S_OK != (hr = Read(ich.stream))) return hr;
                    if(S_OK != (hr = Read(ich.ptrNext))) return hr;
                    int stream = GetMasterStream();
                    while(ich.nIndices-- > 0)
                    {
                        UINT16 object_version;
                        if(S_OK != (hr = Read(object_version))) return hr;
                        if(object_version == 0)
                        {
                            CAutoPtr<IndexRecord> ir(new IndexRecord);
                            if(S_OK != (hr = Read(ir->tStart))) return hr;
                            if(S_OK != (hr = Read(ir->ptrFilePos))) return hr;
                            if(S_OK != (hr = Read(ir->packet))) return hr;
                            if(ich.stream == stream) m_irs.AddTail(ir);
                        }
                    }
                    break;
                }
            case '.SUB':
                if(hdr.size > sizeof(hdr))
                {
                    int size = hdr.size - sizeof(hdr);
                    CAutoVectorPtr<char> buff;
                    if(!buff.Allocate(size)) return E_OUTOFMEMORY;
                    char* p = buff;
                    if(S_OK != (hr = Read((BYTE*)p, size))) return hr;
                    for(char* end = p + size; p < end; )
                    {
                        subtitle s;
                        s.name = p; p += s.name.GetLength()+1;
                        CStringA len(p); p += len.GetLength()+1;
                        s.data = CStringA(p, strtol(len, NULL, 10)); p += s.data.GetLength();
                        m_subs.AddTail(s);
                    }
                }
                break;
            }
        }

        ASSERT(hdr.object_id == 'DATA' 
            || GetPos() == pos + hdr.size 
            || GetPos() == pos + sizeof(hdr));

        pos += hdr.size;
        if(pos > GetPos()) 
            Seek(pos);
    }

    return S_OK;
}

#define GetBits(n) GetBits2(n, p, bit_offset, bit_buffer)

unsigned int GetBits2(int n, unsigned char*& p, unsigned int& bit_offset, unsigned int& bit_buffer)
{
    unsigned int ret = ((unsigned int)bit_buffer >> (32-(n)));

    bit_offset += n;
    bit_buffer <<= n;
    if(bit_offset > (32-16))
    {
        p += bit_offset >> 3;
        bit_offset &= 7;
        bit_buffer = (unsigned int)p[0] << 24;
        bit_buffer |= (unsigned int)p[1] << 16;
        bit_buffer |= (unsigned int)p[2] << 8;
        bit_buffer |= (unsigned int)p[3];
        bit_buffer <<= bit_offset;
    }

    return ret;
}

void GetDimensions(unsigned char* p, unsigned int* wi, unsigned int* hi)
{
    unsigned int w, h, c;

    const unsigned int cw[8] = {160, 176, 240, 320, 352, 640, 704, 0};
    const unsigned int ch1[8] = {120, 132, 144, 240, 288, 480, 0, 0};
    const unsigned int ch2[4] = {180, 360, 576, 0};

    unsigned int bit_offset = 0;
    unsigned int bit_buffer = *(unsigned int*)p;
    bswap(bit_buffer);

    GetBits(13);

    GetBits(13);

    w = cw[GetBits(3)];
    if(w == 0)
    {
        do
        {
            c = GetBits(8);
            w += (c << 2);
        }
        while(c == 255);
    }

    c = GetBits(3);

    h = ch1[c];
    if(h == 0)
    {
        c = ((c << 1) | GetBits(1)) & 3;

        h = ch2[c];
        if(h == 0)
        {
            do
            {
                c = GetBits(8);
                h += (c << 2);
            }
            while(c == 255);
        }
    }

    *wi = w;
    *hi = h;    
}

void CRMFile::GetDimensions()
{
    POSITION pos = m_mps.GetHeadPosition();
    while(pos)
    {
        UINT64 filepos = GetPos();

        MediaProperies* pmp = m_mps.GetNext(pos);
        if(pmp->mime == "video/x-pn-Xvideo")
        {
            pmp->width = pmp->height = 0;

            rvinfo rvi = *(rvinfo*)pmp->typeSpecData.GetData();
            rvi.bswap();

            if(rvi.fcc2 != '04VR')
                continue;

            MediaPacketHeader mph;
            while(S_OK == Read(mph))
            {
                if(mph.stream != pmp->stream || mph.len == 0
                    || !(mph.flags&MediaPacketHeader::PN_KEYFRAME_FLAG))
                    continue;

                BYTE* p = mph.pData.GetData();
                BYTE* p0 = p;
                int len = mph.pData.GetCount();

                BYTE hdr = *p++;
                DWORD packetlen = 0, packetoffset = 0;

                if((hdr&0xc0) == 0x40)
                {
                    packetlen = len - (++p - p0);
                }
                else
                {
                    if((hdr&0x40) == 0) p++;

#define GetWORD(var) var = (var<<8)|(*p++); var = (var<<8)|(*p++);

                    GetWORD(packetlen);
                    if((packetlen&0x4000) == 0) {GetWORD(packetlen); packetlen &= 0x3fffffff;}
                    else packetlen &= 0x3fff;

                    GetWORD(packetoffset);
                    if((packetoffset&0x4000) == 0) {GetWORD(packetoffset); packetoffset &= 0x3fffffff;}
                    else packetoffset &= 0x3fff;

#undef GetWORD

                    if((hdr&0xc0) == 0xc0) packetoffset = 0;
                    else if((hdr&0xc0) == 0x80) packetoffset = packetlen - packetoffset;

                    p++;
                }

                len = min(len - (int)(p - p0), (int)(packetlen - packetoffset));

                if(len > 0)
                {
                    ::GetDimensions(p, &pmp->width, &pmp->height);
                    if(rvi.w == pmp->width && rvi.h == pmp->height)
                        pmp->width = pmp->height = 0;
                    break;
                }
            }
        }

        Seek(filepos);
    }
}

int CRMFile::GetMasterStream()
{
    int s = -1;

    POSITION pos = m_mps.GetHeadPosition();
    while (pos)
    {
        MediaProperies* pmp = m_mps.GetNext(pos);
        if (pmp->mime == "video/x-pn-Xvideo")
        {
            return pmp->stream;
        }
        else if (s == -1 && pmp->mime == "audio/x-pn-Xaudio")
        {
            s = pmp->stream;
        }
    }
    return s;
}

// XMediaSplitter.cpp EOF####################################################################################EOF
