from moviepy.editor import VideoFileClip, AudioFileClip
import sys
import os

def merge_audio_from_video(video1_path, video2_path, output_path):
    # 检查输入文件是否存在
    if not os.path.exists(video1_path):
        raise FileNotFoundError(f"视频1文件未找到: {video1_path}")
    if not os.path.exists(video2_path):
        raise FileNotFoundError(f"视频2文件未找到: {video2_path}")

    # 加载视频1和视频2
    video1 = VideoFileClip(video1_path)
    video2 = VideoFileClip(video2_path)

    # 从视频1中提取音频
    audio1 = video1.audio

    # 把提取的音频合并到视频2中
    video2_with_audio1 = video2.set_audio(audio1)

    # 显示进度
    def process_progress(current, total):
        progress = (current / total) * 100
        sys.stdout.write(f"\r进度: {progress:.2f}%")
        sys.stdout.flush()

    # 保存结果并显示进度
    video2_with_audio1.write_videofile(output_path, codec="libx264", audio_codec="aac", logger="bar", verbose=True)
    print("\n合并完成！")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("用法: python script.py <视频1路径> <视频2路径> <输出文件路径>")
    else:
        video1_path = sys.argv[1]
        video2_path = sys.argv[2]
        output_path = sys.argv[3]
        merge_audio_from_video(video1_path, video2_path, output_path)

