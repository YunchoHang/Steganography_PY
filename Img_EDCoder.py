from PIL import Image
import time

# Helper function to convert text to binary
def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

# Helper function to convert binary to text
def binary_to_text(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

# Function to encode the hidden message into an image
def encode_message(image_path, message, output_path):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print("Error: Image file not found. Please provide a valid path.")
        return
    except Exception as e:
        print(f"Error: Unable to open image file. {e}")
        return

    encoded_img = img.copy()
    width, height = img.size
    max_message_length = (width * height * 3) // 8

    if len(message) + 3 > max_message_length:  # Account for "###" as the terminator
        print("Error: Message too long to encode in the given image.")
        return

    message += "###"
    binary_message = text_to_binary(message)
    message_index = 0

    try:
        for x in range(width):
            for y in range(height):
                pixel = list(encoded_img.getpixel((x, y)))
                for i in range(3):
                    if message_index < len(binary_message):
                        pixel[i] = pixel[i] & ~1 | int(binary_message[message_index])
                        message_index += 1
                encoded_img.putpixel((x, y), tuple(pixel))
                if message_index >= len(binary_message):
                    encoded_img.save(output_path)
                    print("Message encoded successfully!")
                    return
    except Exception as e:
        print(f"An error occurred during encoding: {e}")

# Function to decode the hidden message from an image
def decode_message(image_path):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print("Error: Image file not found. Please provide a valid path.")
        return ""
    except Exception as e:
        print(f"Error: Unable to open image file. {e}")
        return ""

    width, height = img.size
    binary_message = ""

    try:
        for x in range(width):
            for y in range(height):
                pixel = list(img.getpixel((x, y)))
                for i in range(3):
                    binary_message += str(pixel[i] & 1)
    except Exception as e:
        print(f"An error occurred during decoding: {e}")
        return ""

    if len(binary_message) % 8 != 0:
        binary_message = binary_message[:-(len(binary_message) % 8)]

    decoded_message = binary_to_text(binary_message)

    if "###" in decoded_message:
        return decoded_message.split("###")[0]

    return "No hidden message found."

# A menu to choose between encoding and decoding
def main():
    print("What do you want to do?")
    print("1. Encode a message")
    print("2. Decode a message")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        # Encoding process
        image_path = input("Enter the path of the image you want to encode: ")
        message = input("Enter the message you want to encode: ")
        output_path = input("Enter the path to save the encoded image (e.g., /path/to/save/encoded_image.png): ")

        # Making sure that the output path ends with a correct image extension
        if not output_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            print("Error: Specify a correct image file extension (e.g., .png, .jpg).")
        else:
            encode_message(image_path, message, output_path)

    elif choice == "2":
        # Decoding process
        image_path_decode = input("Enter the path of the image to decode (e.g., /path/of/encoded/image.png): ")

        # Starting the timer of decoding process
        start_time = time.time()

        decoded_message = decode_message(image_path_decode)

        # Stops the timer
        end_time = time.time()

        # Calculate total time taken
        total_time = end_time - start_time
        minutes = int(total_time // 60)
        seconds = total_time % 60

        # Display the decoded message and the time taken
        print("Decoded Message:", decoded_message)
        print(f"Time taken to decode: {minutes} minute(s) and {seconds:.2f} second(s)")

    else:
        print("Choose 1 or 2.")

# Run the main function
if __name__ == "__main__":
    main()
