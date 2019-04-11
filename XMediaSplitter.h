// XMediaSplitter.h BOF######################################################################################BOF
#pragma once
#include "BaseSplitter.h"       // CBaseSplitterFilter
#include "BaseSplitterFile.h"   // cBaseSplitterFile

#pragma pack(push, 1)

namespace RMFF
{
    typedef struct ChunkHdr
    {
        union
        {
            char    id[4];
            UINT32  object_id;
        };
        UINT32  size;
        UINT16  object_version;
    } ChunkHdr;

    typedef struct
    {
        UINT32  version;
        UINT32  nHeaders;
    } FileHdr;

    typedef struct 
    {
        UINT32 maxBitRate, avgBitRate;
        UINT32 maxPacketSize, avgPacketSize, nPackets;
        UINT32 tDuration, tPreroll;
        UINT32 ptrIndex, ptrData;
        UINT16 nStreams;
        enum flags_t {PN_SAVE_ENABLED=1, PN_PERFECT_PLAY_ENABLED=2, PN_LIVE_BROADCAST=4} flags;
    } Properies;

    typedef struct 
    {
        UINT16 stream;
        UINT32 maxBitRate, avgBitRate;
        UINT32 maxPacketSize, avgPacketSize;
        UINT32 tStart, tPreroll, tDuration;
        CStringA name, mime;
        CArray<BYTE> typeSpecData;
        UINT32 width, height;
    } MediaProperies;

    typedef struct
    {
        CStringA title, author, copyright, comment;
    } ContentDesc;

    typedef struct
    {
        UINT64 pos;
        UINT32 nPackets, ptrNext;
    } DataChunk;

    typedef struct 
    {
        UINT16 len, stream;
        UINT32 tStart;
        UINT8 reserved;
        enum flag_t {PN_RELIABLE_FLAG=1, PN_KEYFRAME_FLAG=2} flags; // UINT8
        CArray<BYTE> pData;
    } MediaPacketHeader;

    typedef struct {
        UINT32 nIndices;
        UINT16 stream;
        UINT32 ptrNext;
    } IndexChunkHeader;

    typedef struct
    {
        UINT32 tStart, ptrFilePos, packet;
    } IndexRecord;
} // namespace RMFF

#pragma pack(pop)

class CRMFile : public CBaseSplitterFile
{
    using CBaseSplitterFile::Read;

    HRESULT Init();
    void GetDimensions();

public:
    CRMFile(IAsyncReader* pAsyncReader, HRESULT& hr);

    template<typename T> HRESULT Read(T& var);
    HRESULT Read(RMFF::ChunkHdr& hdr);
    HRESULT Read(RMFF::MediaPacketHeader& mph, bool fFull = true);

    RMFF::FileHdr m_fh;
    RMFF::ContentDesc m_cd;
    RMFF::Properies m_p;
    CAutoPtrList<RMFF::MediaProperies> m_mps;
    CAutoPtrList<RMFF::DataChunk> m_dcs;
    CAutoPtrList<RMFF::IndexRecord> m_irs;

    typedef struct {CStringA name, data;} subtitle;
    CList<subtitle> m_subs;

    int GetMasterStream();
};

class CXMediaSplitterFilter : public CBaseSplitterFilter
{
public:
    CXMediaSplitterFilter(LPUNKNOWN pUnk, HRESULT* phr);
    virtual ~CXMediaSplitterFilter();

    // This goes in the factory template table to create new instances
    static CUnknown * WINAPI CreateInstance(LPUNKNOWN u, HRESULT *r) { return new CXMediaSplitterFilter(u, r);  }

protected:
    CAutoPtr<CRMFile> m_pFile;
    HRESULT CreateOutputs(IAsyncReader* pAsyncReader);

    bool InitDeliverLoop();
    void SeekDeliverLoop(REFERENCE_TIME rt);
    bool DoDeliverLoop();

    POSITION m_seekpos;
    UINT32 m_seekpacket;
    UINT64 m_seekfilepos;
private:
    class CChapter
    {
    public:
        REFERENCE_TIME m_rt;
        CStringW m_name;
        CChapter(REFERENCE_TIME rt, CStringW name) : m_rt(rt), m_name(name) {}
    };
    CAutoPtrList<CChapter> m_pChapters;
};

// XMediaSplitter.h EOF######################################################################################EOF
