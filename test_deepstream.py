import sys
sys.path.append('../')
import os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GLib, Gst
from common.is_aarch_64 import is_aarch64
from common.bus_call import bus_call

import pyds

# 객체 클래스 ID 정의
PGIE_CLASS_ID_VEHICLE = 0
PGIE_CLASS_ID_BICYCLE = 1
PGIE_CLASS_ID_PERSON = 2
PGIE_CLASS_ID_ROADSIGN = 3
MUXER_BATCH_TIMEOUT_USEC = 33000

# OSD(On Screen Display) 버퍼 프로브를 처리하는 함수
def osd_sink_pad_buffer_probe(pad, info, u_data):
    frame_number = 0
    num_rects = 0

    # GstBuffer를 가져옴
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        print("GstBuffer를 가져올 수 없습니다.")
        return

    # gst_buffer에서 배치 메타데이터를 검색
    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    l_frame = batch_meta.frame_meta_list

    # 각 프레임 메타데이터를 순회
    while l_frame is not None:
        try:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        # 객체 카운터 초기화
        obj_counter = {
            PGIE_CLASS_ID_VEHICLE: 0,
            PGIE_CLASS_ID_PERSON: 0,
            PGIE_CLASS_ID_BICYCLE: 0,
            PGIE_CLASS_ID_ROADSIGN: 0
        }

        frame_number = frame_meta.frame_num
        num_rects = frame_meta.num_obj_meta
        l_obj = frame_meta.obj_meta_list

        # 각 객체 메타데이터를 순회
        while l_obj is not None:
            try:
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break

            obj_counter[obj_meta.class_id] += 1
            obj_meta.rect_params.border_color.set(0.0, 0.0, 1.0, 0.8)  # 객체의 테두리 색상 설정

            try:
                l_obj = l_obj.next
            except StopIteration:
                break

        # 디스플레이 메타 객체 획득
        display_meta = pyds.nvds_acquire_display_meta_from_pool(batch_meta)
        display_meta.num_labels = 1
        py_nvosd_text_params = display_meta.text_params[0]

        # 디스플레이 텍스트 설정
        py_nvosd_text_params.display_text = "프레임 번호={} 객체 수={} 차량 수={} 사람 수={}".format(
            frame_number, num_rects, obj_counter[PGIE_CLASS_ID_VEHICLE], obj_counter[PGIE_CLASS_ID_PERSON])

        py_nvosd_text_params.x_offset = 10
        py_nvosd_text_params.y_offset = 12

        # 폰트 파라미터 설정
        py_nvosd_text_params.font_params.font_name = "Serif"
        py_nvosd_text_params.font_params.font_size = 10
        py_nvosd_text_params.font_params.font_color.set(1.0, 1.0, 1.0, 1.0)

        # 텍스트 배경색 설정
        py_nvosd_text_params.set_bg_clr = 1
        py_nvosd_text_params.text_bg_clr.set(0.0, 0.0, 0.0, 1.0)

        print(pyds.get_string(py_nvosd_text_params.display_text))
        pyds.nvds_add_display_meta_to_frame(frame_meta, display_meta)

        try:
            l_frame = l_frame.next
        except StopIteration:
            break

    return Gst.PadProbeReturn.OK


def main(args):
    # 입력 인자 확인
    if len(args) != 2:
        sys.stderr.write("usage: %s <media file or uri>\n" % args[0])
        sys.exit(1)

    # GStreamer 초기화
    Gst.init(None)

    # GStreamer 요소 생성
    print("파이프라인 생성 \n ")
    pipeline = Gst.Pipeline()

    if not pipeline:
        sys.stderr.write("파이프라인을 생성할 수 없습니다. \n")

    # 파일 읽기 위한 소스 요소 생성
    print("소스 생성 \n ")
    source = Gst.ElementFactory.make("filesrc", "file-source")
    if not source:
        sys.stderr.write("소스를 생성할 수 없습니다. \n")

    # 입력 파일이 elementary h264 스트림 형식이므로 h264 파서 필요
    print("H264 파서 생성 \n")
    h264parser = Gst.ElementFactory.make("h264parse", "h264-parser")
    if not h264parser:
        sys.stderr.write("h264 파서를 생성할 수 없습니다. \n")

    # GPU에서 하드웨어 가속 디코딩을 위해 nvdec_h264 사용
    print("디코더 생성 \n")
    decoder = Gst.ElementFactory.make("nvv4l2decoder", "nvv4l2-decoder")
    if not decoder:
        sys.stderr.write("Nvv4l2 디코더를 생성할 수 없습니다. \n")

    # 스트림을 배치로 변환하는 nvstreammux 인스턴스 생성
    print("스트림 먹서 생성 \n")
    streammux = Gst.ElementFactory.make("nvstreammux", "Stream-muxer")
    if not streammux:
        sys.stderr.write("NvStreamMux를 생성할 수 없습니다. \n")

    # 디코더의 출력에서 추론을 실행하기 위해 nvinfer 사용
    print("인퍼런스 생성 \n")
    pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
    if not pgie:
        sys.stderr.write("pgie를 생성할 수 없습니다. \n")

    # NV12에서 RGBA로 변환하기 위해 convertor 사용
    print("컨버터 생성 \n")
    nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")
    if not nvvidconv:
        sys.stderr.write("nvvidconv를 생성할 수 없습니다. \n")

    # 변환된 RGBA 버퍼에 그리기 위한 OSD 생성
    print("OSD 생성 \n")
    nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
   
   
    if not nvosd:
        sys.stderr.write("nvosd를 생성할 수 없습니다. \n")

    # 최종적으로 OSD 출력
    if is_aarch64():
        print("nv3dsink 생성 \n")
        sink = Gst.ElementFactory.make("nv3dsink", "nv3d-sink")
        if not sink:
            sys.stderr.write("nv3dsink를 생성할 수 없습니다. \n")
    else:
        print("EGLSink 생성 \n")
        sink = Gst.ElementFactory.make("nveglglessink", "nvvideo-renderer")
        if not sink:
            sys.stderr.write("EGLSink를 생성할 수 없습니다. \n")

    # 입력 파일 설정
    print("파일 %s 재생 \n" % args[1])
    source.set_property('location', args[1])

    # 환경 변수를 통해 nvstreammux를 사용하지 않는 경우만 해당 속성 설정
    if os.environ.get('USE_NEW_NVSTREAMMUX') != 'yes':
        streammux.set_property('width', 1920)
        streammux.set_property('height', 1080)
        streammux.set_property('batched-push-timeout', MUXER_BATCH_TIMEOUT_USEC)
    
    # 스트림 배치 크기 설정 및 추론 설정 파일 경로 지정
    streammux.set_property('batch-size', 1)
    pgie.set_property('config-file-path', "dstest1_pgie_config.txt")

    # 파이프라인에 요소 추가
    print("파이프라인에 요소 추가 \n")
    pipeline.add(source)
    pipeline.add(h264parser)
    pipeline.add(decoder)
    pipeline.add(streammux)
    pipeline.add(pgie)
    pipeline.add(nvvidconv)
    pipeline.add(nvosd)
    pipeline.add(sink)

    # 요소들을 연결
    print("파이프라인 내 요소 연결 \n")
    source.link(h264parser)
    h264parser.link(decoder)

    sinkpad = streammux.get_request_pad("sink_0")
    srcpad = decoder.get_static_pad("src")
    srcpad.link(sinkpad)
    streammux.link(pgie)
    pgie.link(nvvidconv)
    nvvidconv.link(nvosd)
    nvosd.link(sink)

    # 이벤트 루프 생성 및 GStreamer 버스 메시지를 이벤트 루프에 전달
    loop = GLib.MainLoop()
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", bus_call, loop)

    # OSD 요소의 sink 패드에 프로브 추가
    osdsinkpad = nvosd.get_static_pad("sink")
    osdsinkpad.add_probe(Gst.PadProbeType.BUFFER, osd_sink_pad_buffer_probe, 0)

    # 재생 시작 및 이벤트 수신
    print("파이프라인 시작 \n")
    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except:
        pass

    # 정리
    pipeline.set_state(Gst.State.NULL)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
