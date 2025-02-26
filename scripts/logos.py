import re
import os
from PIL import Image, ImageDraw, ImageFont

def create_channel_card(channel_name, output_path, text_color=(255, 0, 255), width=1920, height=1080):  # 16:9 ratio
    # Create black background
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)
    
    # Use a bold system font
    font_path = '/System/Library/Fonts/Helvetica.ttc'
    title_font = ImageFont.truetype(font_path, 300)  # XXX text at 300px
    name_font = ImageFont.truetype(font_path, 120)   # Channel name at 240px
    
    # Always draw "XXX" at the top
    title_text = "XXX"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    
    # Clean up channel name
    clean_name = channel_name.replace("XXX - ", "")  # Remove prefix
    clean_name = re.sub(r'\s*\([^)]*\)', '', clean_name)  # Remove parentheses and contents
    clean_name = clean_name.replace("_", " ")  # Replace underscores with spaces
    
    # Calculate text layout for channel name
    words = clean_name.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=name_font)
        if bbox[2] - bbox[0] > width - 100:  # margin
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(test_line)
                current_line = []
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Calculate total height of all text
    total_text_height = title_height + (len(lines) * (name_font.size + 20))
    
    # Calculate starting Y position to center everything vertically
    y_start = (height - total_text_height) / 2
    
    # Draw XXX text
    draw.text(((width - title_width) / 2, y_start), title_text, font=title_font, fill=text_color)
    
    # Draw channel name lines
    y_position = y_start + title_height + 40  # space after XXX
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=name_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, y_position), line, font=name_font, fill=text_color)
        y_position += name_font.size + 20  # space between lines
    
    # Save the image
    img.save(output_path)

def extract_xxx_channels(m3u_content):
    # Bright pink color
    TEXT_COLOR = (255, 0, 255)  # Pure magenta
    
    channel_info = []
    current_chno = None
    
    for line in m3u_content.split('\n'):
        if 'tvg-chno="' in line:
            match = re.search(r'tvg-chno="(\d+)"', line)
            if match:
                current_chno = match.group(1)
                
            if 'tvg-name="XXX -' in line:
                name_match = re.search('tvg-name="([^"]+)"', line)
                if name_match and current_chno:
                    channel_info.append((name_match.group(1), TEXT_COLOR, current_chno))
                    
    return channel_info

# Create logos directory if it doesn't exist
os.makedirs('logos', exist_ok=True)

# Read the M3U file content
with open('m3u.m3u', 'r') as file:
    m3u_content = file.read()

# Get the channel names and numbers
channel_info = extract_xxx_channels(m3u_content)

# Process all channels
for channel_name, text_color, chno in channel_info:
    output_path = f"logos/{chno}.png"  # Use channel number as filename
    create_channel_card(channel_name, output_path, text_color=text_color)
