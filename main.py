from streaming.env_stream import sensor_stream

def main():
    for data in sensor_stream():
        print(data)

if __name__ == "__main__":
    main()
