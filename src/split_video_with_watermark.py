
import os
import numpy as np
from moviepy import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip

class SplitVideoWithWatermark():
    def __init__(self):
        self.destination_folder = '../data' 
    
    # Define the animation function for position
    def move_watermark(self, t):
        # Define the positions for the watermark (top-left, top-right, bottom-right, bottom-left)
        positions = [
            ('left', 'top'),  
            ('top'),               
            ('right', 'top'),               
            ('right'),               
            ('right', 'bottom'),               
            ('bottom'),                        
            ('left', 'bottom'),                    
            ('left')     
            #('center'),       
        ]
    
        # Cycle through the positions
        return positions[int(np.floor(t / 0.5) % 8)]  # Modulo 8 to loop through the positions

 
    def execute(self, input_video, part_duration, watermark_text):
        """
        Splits a video into parts of a specified duration and adds a watermark to each part.

        Args:
            input_video (str): Path to the input video file.
            part_duration (int): Duration of each part in seconds.
            watermark_text (str): Text to use as the watermark.
        """
        # Ensure output directory exists
        os.makedirs(f'{self.destination_folder}/{input_video}', exist_ok=True)
        
        # Load the video file
        video = VideoFileClip(f'{self.destination_folder}/{input_video}.mp4')
        video_duration = video.duration
        part_index = 1

        for start_time in range(0, int(video_duration), part_duration):
            end_time = min(start_time + part_duration, video_duration)
            part = video.subclipped(start_time, end_time)
            
            watermark = TextClip(
                text=watermark_text, 
                font='ALGER.TTF', 
                font_size=16, 
                color='aqua'
            ).with_duration(part.duration).with_position('center').with_opacity(0.5)
            
            # Set the position of the watermark to follow the movement function
            watermark = watermark.with_position(lambda t: self.move_watermark(t))

            # Combine the video with the animated watermark
            watermarked_part = CompositeVideoClip([part, watermark])

            # Combine the video part with all watermark text clips
            #watermarked_part = CompositeVideoClip([part, watermark_top_left, watermark_top_right, watermark_bottom_left, watermark_bottom_right, watermark_center])

            # Define output path for the part
            part_filename = os.path.join(f'{self.destination_folder}/{input_video}', f"{input_video}_part_{part_index}.mp4")
            print(f"Writing {part_filename} from {start_time:.2f} to {end_time:.2f} seconds")
            watermarked_part.write_videofile(part_filename, codec="libx264", audio_codec="aac")

            part_index += 1
            
            return
                        
        video.close()

    def generate_srt(self, video_file, output_srt):
        """
        Generates a .srt subtitle file with timestamps for a video file.

        Args:
            video_file (str): Path to the video file.
            output_srt (str): Path to save the generated .srt file.
        """
        # Load the video file
        video = VideoFileClip(f'{self.destination_folder}/{video_file}.mp4')
        video_duration = video.duration

        # Open the output .srt file
        with open(output_srt, 'w', encoding='utf-8') as srt_file:
            current_time = 0
            subtitle_index = 1

            while current_time < video_duration:
                # Calculate start and end times for each subtitle (e.g., 5-second intervals)
                start_time = current_time
                end_time = min(current_time + 5, video_duration)

                # Format timestamps
                start_timestamp = self.format_timestamp(start_time)
                end_timestamp = self.format_timestamp(end_time)

                # Write subtitle block
                srt_file.write(f"{subtitle_index}\n")
                srt_file.write(f"{start_timestamp} --> {end_timestamp}\n")
                srt_file.write(f"Subtitle text for segment {subtitle_index}\n\n")

                # Increment time and index
                current_time += 5
                subtitle_index += 1

        # Close the video file
        video.close()

    def format_timestamp(self, seconds):
        """
        Formats a time in seconds to SRT timestamp format (hh:mm:ss,ms).

        Args:
            seconds (float): Time in seconds.

        Returns:
            str: Formatted timestamp string.
        """
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    # Example usage
    def __call__(self):
        input_video = "wheel_of_time_s01_e01"  # Replace with your input video file

        part_duration = 239  # Duration of each part in seconds (4 minutes)
        watermark_text = "TIPSPESA"  # Replace with your watermark text

        self.execute(input_video, part_duration, watermark_text)

SplitVideoWithWatermark()()