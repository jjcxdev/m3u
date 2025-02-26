import re

def update_logo_urls(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as f:
        content = f.read()

    # Define the base URL for the logos
    base_url = "https://raw.githubusercontent.com/jjcxdev/m3u/main/logos/"

    # Regular expression to find and replace logo URLs
    # This looks for the tvg-chno and tvg-logo in the same line
    pattern = r'(tvg-chno="(\d+)".*?tvg-logo=")([^"]*?)(")'
    
    def replace_url(match):
        # Get the channel number from the match
        chno = match.group(2)
        # Construct new URL with the channel number
        return f'{match.group(1)}{base_url}{chno}.png{match.group(4)}'

    # Replace all matching URLs
    updated_content = re.sub(pattern, replace_url, content)

    # Write the updated content to the output file
    with open(output_file, 'w') as f:
        f.write(updated_content)

# Use the function
update_logo_urls('xxx.m3u', 'xxx_updated.m3u')
