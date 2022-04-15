from pipeline.utils.utils import Utils

if __name__ == "__main__":
    frames = Utils().openObject("voorbeeld")
    squat = Utils().augmentation(frames[0], 20)
    for i in squat:
        print(i[0])
    print(len(squat))
