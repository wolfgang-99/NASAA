import imghdr


def is_image_file(file_path):
    # Check if the file is an image using imghdr
    valid_image_extensions = {'jpeg', 'png', 'gif', 'bmp', 'jpg'}
    file_type = imghdr.what(file_path)
    return file_type in valid_image_extensions


def calculate_percentage(current_amount, stated_amount):
    # Prevent division by zero
    if stated_amount == 0:
        return 100 if current_amount == 0 else 0

    # Calculate the percentage
    percentage = (current_amount / stated_amount) * 100

    # Clamp the percentage between 0 and 100
    return max(0, min(percentage, 100))