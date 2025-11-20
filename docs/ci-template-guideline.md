# Hướng dẫn sử dụng Template CI

## Cấu hình tập tin .gitlab-ci.yaml sử dụng Template CI

- Mỗi một dịch vụ trong ứng dụng sẽ có một tập tin `.gitlab-ci.yml`.
- Nội dung của tập tin `.gitlab-ci.yml` chứa các thông tin như sau:

```
# Thêm Template CI do phòng QTUD định nghĩa
include:
- project: qtud/template
  ref: main
  file: ci-template/ci-template.yml

# Chỉ định Global Variable cho quá trình chạy CI Pipeline
variables:
  APPLICATION_NAME:           # Name of Application
  SERVICE_NAME:               # Name of Service
  LOCAL_REGISTRY:             # URL registry
  EXTERNAL_REGISTRY:          # 3rd-party URL registry
  EXTERNAL_REGISTRY_ENV:      # Determine which branch will trigger CI pipeline to push image to 3rd-party Registry
  REGISTRY_USERNAME:          # Name of Registry user (department)
  REGISTRY_PASSWORD:          # Name of Registry password ( department_user)
  EXTERNAL_REGISTRY_USERNAME: # Name of 3rd-party Registry user (department)
  EXTERNAL_REGISTRY_PASSWORD: # Name of 3rd-party Registry password (department_user)
  ARTIFACT_USERNAME:          # Name of Artifact user (department)
  ARTIFACT_PASSWORD:          # Name of Artifact Password ( department_user)
  CI_PROJECT_DIR:             # Context of folder build CI
  DOCKERFILE_NAME:            # Context of Dockerfile
  FILE_EXTENSION:             # Only using with Application VM
  RUNNER_TAG:                 # Name of department
  PLATFORM_TYPE:              # Deployment platform (Container or VM)
  ARTIFACT_BUILD_CI:          # Path build CI -> path source (Gitlab Server) -> build image (download artifact_build_ci)
  ARGUMENTS: |                # Only using with build Container arg
    ENV1=VALUE1
    ENV2=VALUE2

# Định nghĩa các bước thực thi trong quá trình chạy CI pipeline
stages:
  - build
  - codeprotection
  - containerization
  - publish

# Build Artifact cho ứng dụng
build:
  stage: build
  image: maven:3.9.5-eclipse-temurin-21-alpine
  cache: 
    paths:
    - .m2/repository/
  artifacts: 
    expire_in: 8h
    paths:
      - target/$SERVICE_NAME*.jar
  script: 
    - mvn -s maven/settings.xml --batch-mode -U clean package -DskipTests -Djava.awt.headless=true -Dmaven.repo.local=.m2/repository
  tags: 
    - QTUD
  allow_failure: false
```

### Diễn giải chi tiết `.gitlab-ci.yml`

```
# Thêm Template CI do phòng QTUD định nghĩa
include:
- project: qtud/template
  ref: main
  file: ci-template/ci-template.yml
```

- Đây là thông tin Template CI do phòng QTUD định nghĩa được thêm vào trong tập tin `.gitlab-ci.yml` phục vụ cho quá trình CI.
- Trong Template CI sẽ định nghĩa các Job thuộc các Stage `containerization` và `publish`.

```
# Chỉ định Global Variable cho quá trình chạy CI Pipeline
variables:
  APPLICATION_NAME:           # Name of Application
  SERVICE_NAME:               # Name of Service
  LOCAL_REGISTRY:             # URL registry
  EXTERNAL_REGISTRY:          # 3rd-party URL registry
  EXTERNAL_REGISTRY_ENV:      # Determine which branch will trigger CI pipeline to push image to 3rd-party Registry
  REGISTRY_USERNAME:          # Name of Registry user (department)
  REGISTRY_PASSWORD:          # Name of Registry password ( department_user)
  EXTERNAL_REGISTRY_USERNAME: # Name of 3rd-party Registry user (department)
  EXTERNAL_REGISTRY_PASSWORD: # Name of 3rd-party Registry password (department_user)
  ARTIFACT_USERNAME:          # Name of Artifact user (department)
  ARTIFACT_PASSWORD:          # Name of Artifact Password ( department_user)
  CI_PROJECT_DIR:             # Context of folder build CI
  DOCKERFILE_NAME:            # Context of Dockerfile
  FILE_EXTENSION:             # Only using with Application VM
  RUNNER_TAG:                 # Name of department
  PLATFORM_TYPE:              # Deployment platform (Container or VM)
  ARTIFACT_BUILD_CI:          # Path build CI -> path source (Gitlab Server) -> build image (download artifact_build_ci)
  ARGUMENTS: |                # Only using with build Container arg
    ENV1=VALUE1
    ENV2=VALUE2
```

- Cấu hình tùy chỉnh của người dùng được sử dụng trong quá trình CI.
  - **APPLICATION_NAME**: Tên của ứng dụng.
  - **SERVICE_NAME**: Tên của từng dịch vụ trong ứng dụng.
  - **LOCAL_REGISTRY**: URL của Harbor đặt tại nội bộ VNPAY, sử dụng cho việc lưu trữ Docker Image. Mặc định là `registry.vnpay.vn`.
  - **REGISTRY_USERNAME**: Tên tài khoản người dùng sử dụng để truy cập vào Registry nằm trong nội bộ VNPAY. Thông tin này có thể được cấu hình dưới dạng biến của Gitlab, khi đó không cần phải cấu hình trong `.gitlab-ci.yml`.
  - **REGISTRY_PASSWORD**: Mật khẩu tài khoản người dùng sử dụng để truy cập vào Registry nằm trong nội bộ VNPAY. Thông tin này có thể được cấu hình dưới dạng biến của Gitlab, khi đó không cần phải cấu hình trong `.gitlab-ci.yml`.
  - **EXTERNAL_REGISTRY**: URL của Registry nằm ngoài VNPAY.
  - **EXTERNAL_REGISTRY_ENV**: Xác định nhánh được sử dụng để chạy CI đẩy Docker Image lên Registry nằm ngoài VNPAY.
    - Khi người dùng muốn thực hiện CI từ nhánh `develop` để đẩy Docker Image, cần cấu hình `EXTERNAL_REGISTRY_ENV: sit`.
    - Khi người dùng muốn thực hiện CI từ nhánh `releases/*` để đẩy Docker Image, cần cấu hình `EXTERNAL_REGISTRY_ENV: uat`.
  - **EXTERNAL_REGISTRY_USERNAME**: Tên tài khoản người dùng sử dụng để truy cập vào Registry nằm ngoài VNPAY. Thông tin này có thể được cấu hình dưới dạng biến của Gitlab, khi đó không cần phải cấu hình trong `.gitlab-ci.yml`.
  - **EXTERNAL_REGISTRY_PASSWORD**: Mật khẩu tài khoản người dùng sử dụng để truy cập vào Registry nằm ngoài VNPAY. Thông tin này có thể được cấu hình dưới dạng biến của Gitlab, khi đó không cần phải cấu hình trong `.gitlab-ci.yml`.
  - **LOCAL_ARTIFACT**: URL của Nexus đặt tại nội bộ VNPAY, sử dụng cho việc lưu trữ các gói, thư viện do đội Developer phát triển hoặc kéo từ bên ngoài Internet về. Mặc định là `artifact.vnpay.vn`.
  - **ARTIFACT_USERNAME**: Tên tài khoản người dùng sử dụng để truy cập vào Nexus nội bộ VNPAY, được cấp phát theo phòng ban. Thông tin này có thể được cấu hình dưới dạng biến của Gitlab, khi đó không cần phải cấu hình trong `.gitlab-ci.yml`.
  - **ARTIFACT_PASSWORD**: Mật khẩu tài khoản người dùng sử dụng để truy cập vào Nexus nội bộ VNPAY, được cấp phát theo phòng ban. Thông tin này có thể được cấu hình dưới dạng biến của Gitlab, khi đó không cần phải cấu hình trong `.gitlab-ci.yml`.
  - **FILE_EXTENSION**: Phần mở rộng của tập tin được build ra sau khi biên dịch mã nguồn. Nếu sau quá trình biên dịch mã nguồn không có phần mở rộng tập tin thì để rỗng `""`.
    - **Ví dụ**: `jar` là phần mở rộng của các tập tin được biên dịch từ mã nguồn Java.
  - **RUNNER_TAG**: Chỉ định Runner để thực thi Job.
    - `QTUD`: Phòng Quản trị ứng dụng.
    - `THHT`: Phòng Tích hợp hệ thống.
    - `AICNDL`: Phòng AI & Công nghệ dữ liệu.
    - `DVNH`: Phòng Dịch vụ ngân hàng.
    - `DVTCDT`: Phòng Dịch vụ tích hợp tài chính điện tử.
    - `DVTT`: Phòng Dịch vụ trực tuyến.
    - `NDS`: Phòng Nội dung số.
  - **PLATFORM_TYPE**: Khai báo nền tảng triển khai dịch vụ:
    - `container`: Dịch vụ được triển khai dưới dạng Container.
    - `vm`: Dịch vụ được triển khai dưới dạng VM (`systemd`).
  - **ARTIFACT_BUILD_CI**: Đường dẫn lưu trữ các tập tin được build ra sau quá trình biên dịch mã nguồn.
  - **ARGUMENTS**: Cho phép người dùng cấu hình các tham số `ARG` trong Dockerfile trong quá trình build Docker Image.
  
```
# Định nghĩa các bước thực thi trong quá trình chạy CI pipeline
stages:
  - build
  - codeprotection
  - containerization
  - publish
```

- Định nghĩa các Stage để thực thi các Job trong Pipeline CI.
- Mục tiêu của từng Stage:
  - `build`: Là bước thực hiện biên dịch mã nguồn thành bản build (Tập tin Artifact). Đối với các dịch vụ chạy dưới dạng Container, bước này có thể viết trực tiếp trong `Dockerfile` chạy trong Stage `containerization`.
  - `codeprotection`: Là bước thực hiện bảo vệ mã nguồn. Có thể không cần khai báo nếu không sử dụng.
  - `containerization`: Là bước thực hiện đóng gói Docker Image phục vụ cho việc triển khai các dịch vụ chạy dưới dạng Container. **Khi sử dụng Template CI của phòng QTUD thì bắt buộc phải khai báo Stage này**.
  - `publish`: Là bước đẩy tập tin Artifact hoặc Docker Image lên trên hệ thống lưu trữ, đồng thời gửi các thông tin tới hệ thống SRE-BOT để xử lý tiến trình CD. **Khi sử dụng Template CI của phòng QTUD thì bắt buộc phải khai báo Stage này**.

```
# Build Artifact cho ứng dụng
build:
  stage: build
  image: maven:3.9.5-eclipse-temurin-21-alpine
  cache: 
    paths:
    - .m2/repository/
  artifacts: 
    expire_in: 8h
    paths:
      - target/$SERVICE_NAME*.jar
  script: 
    - mvn -s maven/settings.xml --batch-mode -U clean package -DskipTests -Djava.awt.headless=true -Dmaven.repo.local=.m2/repository
  tags: 
    - QTUD
  allow_failure: false
```

- Các Job thực hiện trong Stage `build` tùy thuộc vào nhu cầu và cách thức thực hiện của từng đội Developer. 