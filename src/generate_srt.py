from moviepy.video.io.VideoFileClip import VideoFileClip
import os

class GenerateSRT():
    def __init__(self):
        self.destination_folder = '../data' 
    
    def generate(self, video_file):
        """
        Generates a .srt subtitle file with timestamps for a video file.

        Args:
            video_file (str): Path to the video file.
        """
        # Load the video file
        video = VideoFileClip(f'{self.destination_folder}/{video_file}.mp4')
        video_duration = video.duration

        # Open the output .srt file
        with open(f'{self.destination_folder}/{video_file}.srt', 'w', encoding='utf-8') as srt_file:
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
        video_file = f'wheel_of_time_s01_e01/wheel_of_time_s01_e01_part_2'  # Replace with your input file path without the suffix .mp4
        self.generate(video_file)

GenerateSRT()()