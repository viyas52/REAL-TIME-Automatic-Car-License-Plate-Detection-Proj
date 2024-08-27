import torch

cuda_available = torch.cuda.is_available()
print(f"CUDA Available: {cuda_available}")

if cuda_available:
    
    gpu_name = torch.cuda.get_device_name(0)
    print(f"GPU in Use: {gpu_name}")
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Current CUDA Device: {device}")

    cuda_version = torch.version.cuda
    print(f"CUDA Version: {cuda_version}")

    cudnn_version = torch.backends.cudnn.version()
    print(f"cuDNN Version: {cudnn_version}")
else:
    print("CUDA is not available on this system.")
