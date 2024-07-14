from PIL import Image
image_path = "C://Users//tatat//Downloads//openai_simple_outpainting-master (1)//openai_simple_outpainting-master//sample//sample_img.jpg"
new_image = Image.open(image_path)

# Create a new transparent canvas
canvas_size = (2042, 1021)
new_canvas = Image.new("RGBA", canvas_size, (255, 255, 255, 0))

# Calculate position to center the new image on the canvas
new_image_size = new_image.size
position = ((canvas_size[0] - new_image_size[0]) // 2, (canvas_size[1] - new_image_size[1]) // 2)

# Paste the new image onto the transparent canvas
new_canvas.paste(new_image, position, new_image.convert("RGBA"))

# Save the resulting image
new_output_path1 = "C:/Users/tatat/Downloads/openai_simple_outpainting-master (1)/openai_simple_outpainting-master/src/src.png"
new_output_path2 = "C:/Users/tatat/Downloads/openai_simple_outpainting-master (1)/openai_simple_outpainting-master/src/mask.png"
new_output_path3 = "C:/Users/tatat/Downloads/openai_simple_outpainting-master (1)/openai_simple_outpainting-master/src/sample.png"
new_canvas.save(new_output_path1)
new_canvas.save(new_output_path2)
new_canvas.save(new_output_path3)

new_output_path1
new_output_path2
new_output_path3