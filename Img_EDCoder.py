from PIL import Image
import time

# Function to encode the hidden message into an image
def encode_message(image_path, message, output_path):
    # Opens the image
    img = Image.open(image_path)
    encoded_img = img.copy()
    width, height = img.size


    message += "###" 
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    message_index = 0

    for x in range(width):
        for y in range(height):
            pixel = list(encoded_img.getpixel((x, y)))
            for i in range(3): 
                if message_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[message_index])
                    message_index += 1
            encoded_img.putpixel((x, y), tuple(pixel))
            if message_index >= len(binary_message):
		# Saves the image
                encoded_img.save(output_path)
                print("Message encoded successfully!")
                return

    print("Message too long to encode in the given image.")

# Function to decode the hidden message from an image
def decode_message(image_path):
    img = Image.open(image_path)
    width, height = img.size
    binary_message = ""
    

    for x in range(width):
        for y in range(height):
            pixel = list(img.getpixel((x, y)))
            for i in range(3):  
                binary_message += str(pixel[i] & 1)


    if len(binary_message) % 8 != 0:
        binary_message = binary_message[:-(len(binary_message) % 8)]  

   
    decoded_message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

   
    if "###" in decoded_message:
        return decoded_message.split("###")[0]  
    
    return "No hidden message found."


# A menu to choose between encoding and decoding
def main():
    print("What do you what to do?")
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
