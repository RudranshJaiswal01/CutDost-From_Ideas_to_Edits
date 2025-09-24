import numpy as np
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
import moviepy.video.fx.all as vfx

# Load main video
video = VideoFileClip('uploads/main_video.mp4')

# Sepia filter function
def sepia(frame):
    frame = frame.astype(np.float32)
    r = frame[..., 0]
    g = frame[..., 1]
    b = frame[..., 2]
    tr = 0.393 * r + 0.769 * g + 0.189 * b
    tg = 0.349 * r + 0.686 * g + 0.168 * b
    tb = 0.272 * r + 0.534 * g + 0.131 * b
    sepia_frame = np.stack([tr, tg, tb], axis=-1)
    sepia_frame = np.clip(sepia_frame, 0, 255).astype(np.uint8)
    return sepia_frame

# Create subclips
clip0 = video.subclip(0, 2)
clip1 = video.subclip(2, 4)
clip2 = video.subclip(4, 9)
clip3 = video.subclip(9, 11)
clip4 = video.subclip(11, 16)
clip5 = video.subclip(16, 20)

# Apply sepia to first 4 seconds
clip0 = clip0.fl_image(sepia)
clip1 = clip1.fl_image(sepia)

# Smooth zoom on face (clip0) – from 1x to 1.2x
clip0 = clip0.fx(vfx.resize, lambda t: 1 + 0.1 * t)

# Smooth zoom on cat (clip2, clip3, clip4) – from 1x to 1.3x
clip2 = clip2.fx(vfx.resize, lambda t: 1 + 0.3 * (t / clip2.duration))
clip3 = clip3.fx(vfx.blackwhite).fx(vfx.resize, lambda t: 1 + 0.3 * (t / clip3.duration))
clip4 = clip4.fx(vfx.resize, lambda t: 1 + 0.3 * (t / clip4.duration))

# Fade‑in at start and fade‑out at end
clip0 = clip0.fx(vfx.fadein, 1)
clip5 = clip5.fx(vfx.fadeout, 1)

# Concatenate all parts
final = concatenate_videoclips([clip0, clip1, clip2, clip3, clip4, clip5], method='compose')

# Watermark
watermark = (TextClip('edited with ai', fontsize=24, color='white', font='Arial')
             .set_opacity(0.5)
             .set_position(('right', 'bottom'))
             .set_duration(final.duration))

# Subtitles data (seconds)
subtitles = [
    {'start': 0, 'end': 2, 'text': 'YO, why does he actually sound like a squeaky toy?'},
    {'start': 2, 'end': 4, 'text': 'I raised you my human.'},
    {'start': 4, 'end': 16, 'text': "my cat, squeaky toy. Oh my god! You're so cute!"},
    {'start': 16, 'end': 20, 'text': ''}
]

subtitle_clips = []
for sub in subtitles:
    if sub['text'].strip():
        txt = (TextClip(sub['text'], fontsize=30, color='white', font='Arial',
                        stroke_color='black', stroke_width=2, method='caption',
                        size=(video.w, None), align='center')
               .set_position(('center', 'bottom'))
               .set_start(sub['start'])
               .set_duration(sub['end'] - sub['start']))
        subtitle_clips.append(txt)

# Composite final video with watermark and subtitles
final_video = CompositeVideoClip([final, watermark] + subtitle_clips)

# Write output file
final_video.write_videofile('output.mp4', codec='libx264', audio_codec='aac', fps=video.fps)

# Release resources
final_video.close()
video.close()