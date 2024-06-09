import os
from cog import BasePredictor, Input, Path
from argparse import Namespace
import pose_align as p
import subprocess
from moviepy.editor import VideoFileClip, AudioFileClip

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load any necessary model weights into memory"""
        import downloading_weights  # Ensure this script downloads weights if not present

    def predict(
        self,
        imgfn_refer: Path = Input(description="Reference image path"),
        vidfn: Path = Input(description="Input video path"),
        detect_resolution: int = Input(description="Detection resolution", default=512),
        image_resolution: int = Input(description="Image resolution", default=720),
        align_frame: int = Input(description="Frame to align to", default=0),
        max_frame: int = Input(description="Maximum number of frames to process", default=300),
    ) -> Path:
        """Run pose alignment on the input video based on the reference image"""
        args = Namespace(
            detect_resolution=detect_resolution,
            image_resolution=image_resolution,
            yolox_config="./pose/config/yolox_l_8xb8-300e_coco.py",
            dwpose_config="./pose/config/dwpose-l_384x288.py",
            yolox_ckpt="./pretrained_weights/dwpose/yolox_l_8x8_300e_coco.pth",
            dwpose_ckpt="./pretrained_weights/dwpose/dw-ll_ucoco_384.pth",
            align_frame=align_frame,
            max_frame=max_frame,
            imgfn_refer=str(imgfn_refer),
            vidfn=str(vidfn),
            outfn_align_pose_video=None,
            outfn=None,
        )

        # Ensure the output directories exist
        if not os.path.exists("./assets/poses/align"):
            os.makedirs("./assets/poses/align")
            os.makedirs("./assets/poses/align_demo")

        # Generate output file paths based on input filenames
        if args.outfn_align_pose_video is None:
            args.outfn_align_pose_video = f"./assets/poses/align/img_ref_video_dance.mp4"
        if args.outfn is None:
            args.outfn = f"./assets/poses/align_demo/img_ref_video_dance.mp4"

        # Run the pose alignment process
        p.run_align_video_with_filterPose_translate_smooth(args)

        # 定义命令及其参数
        command = [
            "python", "gen.py",
            "--config", "./configs/test_stage_2.yaml",
        ]

        # 执行命令
        result = subprocess.run(command, capture_output=True, text=True)
        # 输出结果
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # 定义命令及其参数
        mergeCommand = [
            "python", "merge_audio.py", args.vidfn, "output/video_no_audio.mp4", "video_and_audio.mp4",
        ]
        # 执行命令
        mergeResult = subprocess.run(mergeCommand, capture_output=True, text=True)
        print("STDOUT:", mergeResult.stdout)
        print("STDERR:", mergeResult.stderr)
        
        return Path("video_and_audio.mp4")

