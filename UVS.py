# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:54:46 2020

@author: AsteriskAmpersand
"""
import construct as C

Header = C.Struct(
        "uvsSignature" / C.Const(b"UVS\x00"),
        "ibSignature" / C.Const([0,7,18,22] ,C.Byte[4]), 
        "groupOffset" / C.Int64sl,
        "groupCount" / C.Int64sl,
        "stringOffset" / C.Int64sl,
        "stringCount" / C.Int64sl
        )

Primary = C.Struct(
        "uv0" / C.Float32l[2],
        "uv1" / C.Float32l[2],
        "unkn" / C.Float32l[4],       
        )
defaultPrimary = {
        "unkn" : [0.5,0.5,0,0]
        }

MapIndices = C.Struct(
        "pathIndex" / C.Int32sl[4],
        )

GroupHead = C.Struct(
        "frameDataOffset" / C.Int64sl,
        "frameCount" /  C.Int64sl,
        "frameIndexOffset" /  C.Int64sl,
        "frameIndexCount" /  C.Int64sl,
        "dataOffset" / C.Int64sl,
        "mapCount" /  C.Int64sl,
        "unkn32_0" /  C.Float32l,
        "unkn32_1" / C.Float32l,
        "unkn3" /  C.Int64sl,
        )

MetaFrameIndex = lambda x: C.Struct("frameIndices" / C.Int32sl[x])
MapIndex = C.Struct("mapIndices" / C.Int32sl[4])
Group = C.Struct(
        "frameDataOffset" / C.Int64sl,
        "frameCount" /  C.Int64sl,
        "frameIndexOffset" /  C.Int64sl,
        "frameIndexCount" /  C.Int64sl,
        "dataOffset" / C.Int64sl,
        "mapCount" /  C.Int64sl,
        "unkn32_0" /  C.Float32l,
        "unkn32_1" / C.Float32l,
        "unkn3" /  C.Int64sl,
        "frameData" / C.Pointer(C.this.frameDataOffset,Primary[C.this.frameCount]),
        "frameIndex" / C.Pointer(C.this.frameIndexOffset,C.Int32sl[C.this.frameIndexCount]),#32-Padded to next
        "mapIndices" / C.IfThenElse(C.this.frameCount != 0,
             C.Pointer(C.this.dataOffset,C.Int32sl[4]),
             C.Int32sl[0]
             ),
        )

def defaultMapIndices(l): return l+[0]*(4-len(l))

StringHead = C.Struct(
        "blank" /  C.Int64sl,
        "stringOffset" /  C.Int64sl,
        "type" /  C.Int32sl)
StringBody = C.Struct(
        "string" / C.CString("utf-8"),
        )
StringData = C.Struct(
        "blank" /  C.Int64sl,
        "stringOffset" /  C.Int64sl,
        "type" /  C.Int32sl,        
        "string" / C.Pointer(C.this.stringOffset,C.CString("utf-8")),
        "padding" / C.Optional(C.Const(0,C.Int32sl))
        )

UVSFile = C.Struct(
        "Header" / Header,
        "Groups" / C.Pointer(C.this.Header.groupOffset,Group[C.this.Header.groupCount]),
        "Strings" / C.Pointer(C.this.Header.stringOffset,StringData[C.this.Header.stringCount])        
        )

def pad(size,offset):
    cursor = offset
    return (-cursor)%size + offset

def bpad(size,data):
    return data + b"\x00"*((-len(data))%size)

def compileRelativeStringOffsets(strings):
    currOffset = 0
    offsets = []
    for s,t in strings:
        offsets.append(currOffset)
        currOffset = pad(4,currOffset+len(s.encode("utf-8"))+1)
    return offsets

def compileRelativeFrameOffsets(frameCounts,groupDataOffset):
    currOffset = groupDataOffset
    frame = []
    index = []
    data = []
    for fc in frameCounts:
        frame.append(currOffset)
        currOffset += 0x20*fc
        index.append(currOffset)
        currOffset = pad(16,currOffset + 0x4*fc)
        data.append(currOffset)
        currOffset += 0x10*(fc != 0)
    return frame,index,data,currOffset

def compileSpacings(groups, strings):
    relativeStringOffsets = compileRelativeStringOffsets(strings)
    groupCount = len(groups)
    stringCount = len(strings)
    frameDataCounts = list(map(lambda x: len(x.framedata),groups))
    groupOffset = 0x30
    groupDataOffset = groupOffset + groupCount*0x40
    frameROffsets, indexROffsets, dataROffsets,stringBlockOffset = compileRelativeFrameOffsets(frameDataCounts,groupDataOffset)
    stringOffset = stringBlockOffset + stringCount*0x18 - 4
    frameDataOffsets = [f for f in frameROffsets]
    indexOffsets = [f for f in indexROffsets]
    dataROffsets = [f for f in dataROffsets]
    stringOffsets = [stringOffset+f for f in relativeStringOffsets]
    return (groupOffset,groupCount,stringBlockOffset,stringCount,\
            frameDataOffsets,frameDataCounts,indexOffsets,frameDataCounts,dataROffsets,\
            stringOffsets)
    
def UVSCompile(header,groupHeaders,groupBlocks,stringBlocks,stringData):
    #bpad
    data = b""
    data += Header.build(header)
    data = bpad(0x10,data)
    data += b''.join([GroupHead.build(gheader) for gheader in groupHeaders])
    for frames,index,datum in groupBlocks:
        if len(frames):
            data += b''.join([Primary.build(f) for f in frames])
            data += MetaFrameIndex(len(index["frameIndices"])).build(index)
            data = bpad(16,data)
            data += MapIndex.build(datum)
    for ix,block in enumerate(stringBlocks):
        data += StringHead.build(block)
        if ix != len(stringBlocks)-1:
            data += b"\x00"*4    
    for ix,string in enumerate(stringData):
        data += StringBody.build(string)
        if ix != len(stringData)-1:
            data = bpad(4,data)
    return data

#Header: GroupOffset, GroupCount, StringOffset, StringCount
#Groups: FrameDataOffset, FrameDataCount, frameIndexOffset, frameIndexCount
#Strings: StringOffset

if __name__ in "__main__":
    from UVGroup import UVGroup
    path = "wp\god_lies_here\shrek"
    groups = []
    dynamic = 4
    fCount = 53121
    sDimensions = 256
    delta = 1/sDimensions
    for j in range(fCount//sDimensions):
        name = path
        framedata = [((i*delta,j*delta),((i+1)*delta,(j+1)*delta))for i in range(sDimensions)]
        tpaths = [path]
        ttypes = [1]
        dynamic = 4
        group = UVGroup(name,framedata,tpaths,ttypes,dynamic)
        groups.append(group)
    paths = [(path,1)]
    for group in groups:
        group.indexize(paths)
    (groupOffset,groupCount,stringOffset,stringCount,
    frameDataOffsets,frameDataCounts,indexOffsets,frameDataCounts,mapIndexOffset,
    stringOffsets) = compileSpacings(groups,paths)
    _Header = {"uvsSignature":b"UVS\x00","ibSignature":[0,7,18,22],
              "groupOffset":groupOffset,"groupCount":groupCount,
              "stringOffset":stringOffset,"stringCount":stringCount}
    _GroupHeaders = [{"frameDataOffset":fdOffset,"frameCount":fCount,
                     "frameIndexOffset":fiOffset,"frameIndexCount":fCount,
                     "dataOffset":dOffset,"mapCount":len(group.types),
                     "unkn32_0":32,"unkn32_1":32,"unkn3":group.dynamic} 
                    for group,fdOffset,fCount,fiOffset,dOffset in 
                    zip(groups,frameDataOffsets,frameDataCounts,indexOffsets,mapIndexOffset)]
    groupPad = lambda x: x + [0]*((-len(x))%4)
    _GroupBlocks = [(  [{"uv0":uv0,"uv1":uv1,"unkn":[.5,.5,0,0]} for uv0,uv1 in group.framedata],
                      {"frameIndices":list(range(len(group.framedata)))},
                      {"mapIndices":groupPad(group.indices) if len(group.framedata) else []})                        
                    for group in groups]
    _StringBlocks = [{"blank":0,"stringOffset":offset,"type":typing} 
                        for offset,(string,typing) in zip(stringOffsets,paths)]
    _StringData = [{"string":string} for string,typing in paths]
    binaryUVS = UVSCompile(_Header,_GroupHeaders,_GroupBlocks,_StringBlocks,_StringData)
    with open(r"E:\Program Files (x86)\Steam\steamapps\common\Monster Hunter World\nativePC\wp\byleth_efx\tests.uvs","wb") as inf:
        inf.write(binaryUVS)


"""
    errors = []
    op = print
    #print = errors.append
    nonPrim = []
    from pathlib import Path
    for inf in Path(r"E:\MHW\chunkG0").rglob("*.uvs"):
        try:
            uvf = UVSFile.parse(inf.open("rb").read())
        except:
            print("%s Failed to Read"%inf)
            raise
        for ex, group in enumerate(uvf.Groups):    
            if group.frameIndexCount > 1:
                nonPrim.append((group.frameIndexCount,inf))
    for i in sorted(nonPrim):
        print (i)

        for ex, group in enumerate(uvf.Groups):
            if group.mapCount == 0:
                print("No Maps: %s"%(str(inf)))
            for ix,s in enumerate(group.frameIndex):
                if ix != s:
                    print("%s Secondary Mismatch %d/%d"%(inf,ix,s))
            if group.frameIndexCount != group.frameCount:
                print("%s Secondary Primary Mismatch"%(inf))
            if group.unkn32_0 != group.unkn32_1 != 32:
                print(inf)
                raise
            if group.unkn3 != 4:
                print("Unkn3: %d != 4 in %s"%(group.unkn3,str(inf)))
                #print("%s Entry ID Mismatch %d/%d"%(inf,ex,group.data.entryID))
        if uvf.Header.stringCount != uvf.Header.groupCount:
            print("%s has Mismatched Counts %d/%d"%(inf,uvf.Header.groupCount,uvf.Header.stringCount))
            pass
        for stringData in uvf.Strings:
            if stringData.blank != 0:
                raise
            if stringData.type != 1:
                #print(inf)
                print("Non Standard Type: %d: %s - %s"%(stringData.type,stringData.string,inf))
                #raise
    
    print = op
    for err in sorted(errors):
        print(err)
"""
        #else:
        #    print(str(inf))
        #for frame in group.frameData:
        #    if frame.unkn != [.5,.5,0,0]:
        #        print(inf)
        #        raise
        #if group.primaryCount == 0:
        #    print("No Primary: %s"%str(inf))
        
        #if group.unkn0 != 1:
        #    print("UNKN MISMATCH 0: %s: %d"%(str(inf),group.unkn0))
        #if group.unkn1 != 32:
        #    print("UNKN MISMATCH 1: %s: %f"%(str(inf),group.unkn1))
        #if group.unkn2 != 32:
        #    print("UNKN MISMATCH 2: %s: %f"%(str(inf),group.unkn2))
        #if group.unkn3 != 1:
        #    print("UNKN MISMATCH 3: %s: %d"%(str(inf),group.unkn3))
    
    #for string in uvf.Strings[:]:
    #    if string.one != 1:
    #        print("%s has Non 1 String One %d"%(inf,string.one))
    #        #raise
