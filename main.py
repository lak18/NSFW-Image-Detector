from nsfw_model.nsfw_detector import predict
model = predict.load_model('C:\\Users\\Lenovo\\Desktop\\nfsw image detector\\nsfw_model\\nsfw_mobilenet2.224x224.h5')

# Predict single image
ans = predict.classify(model, 'Screenshot (14).png')
print(ans)
# {'2.jpg': {'sexy': 4.3454722e-05, 'neutral': 0.00026579265, 'porn': 0.0007733492, 'hentai': 0.14751932, 'drawings': 0.85139805}}

# Predict multiple images at once
# predict.classify(model, ['/Users/bedapudi/Desktop/2.jpg', '/Users/bedapudi/Desktop/6.jpg'])
# # {'2.jpg': {'sexy': 4.3454795e-05, 'neutral': 0.00026579312, 'porn': 0.0007733498, 'hentai': 0.14751942, 'drawings': 0.8513979}, '6.jpg': {'drawings': 0.004214506, 'hentai': 0.013342537, 'neutral': 0.01834045, 'porn': 0.4431829, 'sexy': 0.5209196}}

# # Predict for all images in a directory
# predict.classify(model, '/Users/bedapudi/Desktop/')
