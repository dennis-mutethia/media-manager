from moviepy.video.io.VideoFileClip import VideoFileClip
import os

class SplitMP4():
    def __init__(self):
        self.destination_folder = '../data' 
        
    def split_video(self, input_file, chunk_duration=240):
        """
        Splits an input .mp4 video file into parts of the specified duration.

        Args:
            input_file (str): Path to the input .mp4 file.
            chunk_duration (int): Duration of each part in seconds (default is 240 seconds).
        """
        # Ensure output directory exists
        os.makedirs(f'{self.destination_folder}/{input_file}', exist_ok=True)

        # Load the video file
        video = VideoFileClip(f'{self.destination_folder}/{input_file}.mp4')
        video_duration = video.duration  # Duration in seconds

        print(f"Video duration: {video_duration:.2f} seconds")

        # Iterate through the video and create chunks
        start_time = 0
        part = 1

        while start_time < video_duration:
            end_time = min(start_time + chunk_duration, video_duration)

            # Write the chunk to a file
            output_file = os.path.join(f'{self.destination_folder}/{input_file}', f"{input_file}_part_{part}.mp4")
            print(f"Writing {output_file} from {start_time:.2f} to {end_time:.2f} seconds")

            video.subclipped(start_time, end_time).write_videofile(output_file, codec="libx264", audio_codec="aac")

            start_time = end_time
            part += 1

        # Close the video file
        video.close()

    # Example usage
    def __call__(self):
        input_file = f'wheel_of_time_full_s01_e05'  # Replace with your input file path without the suffix .mp4
        self.split_video(input_file)

SplitMP4()()