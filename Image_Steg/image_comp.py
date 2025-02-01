import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.metrics import structural_similarity as ssim

# Get user input for file paths
original_path = input("Enter the path of the original image: ")
encoded_path = input("Enter the path of the encoded image: ")

# Load images with PIL for display
try:
    original_pil = Image.open(original_path)
    encoded_pil = Image.open(encoded_path)
except FileNotFoundError:
    print("Error: One or both image files not found. Please check the paths.")
    exit()
except Exception as e:
    print(f"Error: Unable to open image file. {e}")
    exit()

# Load images with OpenCV for analysis
original = cv2.imread(original_path)
encoded = cv2.imread(encoded_path)

if original is None or encoded is None:
    print("Error: Unable to load images for pixel difference analysis.")
    exit()

if original.shape != encoded.shape:
    print("Error: Images must have the same dimensions for comparison.")
    exit()

# Convert to grayscale for SSIM calculation
original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
encoded_gray = cv2.cvtColor(encoded, cv2.COLOR_BGR2GRAY)

# Compute absolute difference
diff = cv2.absdiff(original, encoded)
diff_gray = cv2.absdiff(original_gray, encoded_gray)

# Calculate statistics
num_diff_pixels = np.count_nonzero(diff_gray)  # Count changed pixels
total_pixels = original_gray.size  # Total pixels in the image
percent_diff = (num_diff_pixels / total_pixels) * 100  # Percentage of different pixels

mse = np.mean((original_gray.astype("float") - encoded_gray.astype("float")) ** 2)  # Mean Squared Error
ssim_value = ssim(original_gray, encoded_gray)  # Structural Similarity Index

# Print stats
print("\n=== Image Comparison Stats ===")
print(f"Total Pixels: {total_pixels}")
print(f"Changed Pixels: {num_diff_pixels}")
print(f"Difference Percentage: {percent_diff:.2f}%")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Structural Similarity Index (SSIM): {ssim_value:.4f} (1.0 = identical)")

# Display side-by-side images using Matplotlib
plt.figure(figsize=(12, 5))

plt.subplot(1, 3, 1)
plt.imshow(original_pil)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(encoded_pil)
plt.title("Encoded Image")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(diff)
plt.title("Pixel Differences")
plt.axis("off")

plt.show()

# Show difference image in OpenCV window
cv2.imshow("Original Image", original)
cv2.imshow("Encoded Image", encoded)
cv2.imshow("Pixel Differences", diff)

cv2.waitKey(0)
cv2.destroyAllWindows()
