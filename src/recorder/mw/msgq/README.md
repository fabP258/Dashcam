# MSGQ

MSGQ is a lock free single producer multi consumer message queue for inter-process communication using shared memory. It is a stripped down version of Comma.ai's [MSGQ](https://github.com/commaai/msgq).

## Compile the demo
* Publisher

```
g++ publish.cc ipc.cc msgq.cc -o publisher.bin
```

* Subscriber

```
g++ subscribe.cc ipc.cc msgq.cc -o subscriber.bin
```

## Run the demo

1. Start the publisher
```
./publisher.bin
```

2. Start the subscriber
```
./subscriber.bin
```
