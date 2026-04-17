# Hệ thống robot omni tự hành trong môi trường bệnh viện (ROS2)

## Mục lục

-   [Giới thiệu](#giới-thiệu)
-   [Tính năng](#tính-năng)
-   [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
-   [Cấu trúc thư mục](#cấu-trúc-thư-mục)
-   [Cài đặt](#cài-đặt)
-   [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
-   [Thuật toán sử dụng](#thuật-toán-sử-dụng)
-   [Định hướng phát triển](#định-hướng-phát-triển)
-   [Đóng góp](#đóng-góp)
-   [Tác giả](#tác-giả)
-   [Credits](#credits)

------------------------------------------------------------------------

## Giới thiệu

Dự án này xây dựng một hệ thống robot tự hành sử dụng ROS2, có khả năng
hoạt động trong môi trường bệnh viện và thực hiện nhiệm vụ di chuyển qua
nhiều phòng theo thứ tự tối ưu.

Khác với các bài toán điều hướng cơ bản chỉ xử lý một điểm đích, hệ
thống này giải quyết bài toán phức tạp hơn: lập kế hoạch di chuyển qua
nhiều điểm (multi-goal navigation). Bài toán này tương tự như bài toán
người du lịch (TSP), trong đó mục tiêu là tối thiểu hóa tổng quãng đường
di chuyển.

Hệ thống được thiết kế theo hướng mô-đun, tích hợp đầy đủ các thành phần
quan trọng của một hệ thống robot thực tế: SLAM, localization,
navigation, task planning và giao diện người dùng.

------------------------------------------------------------------------

## Tính năng

-   Điều hướng qua nhiều điểm với thứ tự tối ưu
-   Tối ưu lộ trình bằng thuật toán di truyền (Genetic Algorithm)
-   Sử dụng chi phí đường đi thực tế từ Nav2 thay vì khoảng cách hình
    học
-   Tự động tái lập kế hoạch khi gặp vật cản hoặc không thể đến đích
-   Mô phỏng môi trường bệnh viện với nhiều phòng và hành lang phức tạp
-   Giao diện người dùng (GUI) hỗ trợ chọn điểm và giám sát hệ thống

------------------------------------------------------------------------

## Kiến trúc hệ thống

Hệ thống bao gồm các thành phần chính:

-   Gazebo: môi trường mô phỏng
-   Cartographer: xây dựng bản đồ (SLAM)
-   robot_localization (EKF): hợp nhất dữ liệu cảm biến
-   Nav2: lập kế hoạch đường đi và điều khiển robot
-   Genetic Algorithm: tối ưu thứ tự các điểm cần đi
-   Nav Controller: điều phối thực thi và xử lý re-planning
-   GUI (PyQt5): giao diện người dùng

Luồng hoạt động:

1.  Người dùng chọn các phòng cần đi
2.  Thuật toán GA tính toán thứ tự tối ưu
3.  Nav2 lập đường đi chi tiết
4.  Robot thực hiện di chuyển
5.  Nếu xảy ra lỗi → hệ thống tính toán lại lộ trình

------------------------------------------------------------------------

## Cấu trúc thư mục

    robot_omni/
    ├── launch/
    ├── config/
    ├── urdf/
    ├── worlds/
    ├── map/
    ├── rviz/
    ├── models/
    ├── scripts/
    └── CMakeLists.txt

------------------------------------------------------------------------

## Cài đặt

### Yêu cầu

-   ROS2 (khuyến nghị Jazzy)
-   Nav2
-   Cartographer
-   robot_localization
-   Gazebo (ros_gz)
-   Python3 + PyQt5

Cài đặt nhanh:

    sudo apt update
    sudo apt install ros-jazzy-nav2* \
                     ros-jazzy-cartographer* \
                     ros-jazzy-robot-localization \
                     python3-pyqt5

------------------------------------------------------------------------

## Hướng dẫn sử dụng

### Chạy hệ thống

    ros2 launch robot_omni navigation2_old.launch.py

### Chạy giao diện

    python3 scripts/gui.py

Chế độ: - ga: tối ưu lộ trình - sequential: đi theo thứ tự nhập

------------------------------------------------------------------------

## Thuật toán sử dụng

  Thành phần      Phương pháp
  --------------- -------------------
  SLAM            Cartographer
  Localization    EKF
  Navigation      Nav2
  Controller      MPPI
  Task Planning   Genetic Algorithm

------------------------------------------------------------------------

## Định hướng phát triển

-   Hỗ trợ nhiều robot (multi-robot)
-   Tích hợp hệ thống quản lý nhiệm vụ
-   Triển khai trên robot thực
-   Cải thiện xử lý vật cản động

------------------------------------------------------------------------

## Đóng góp

Mọi đóng góp đều được hoan nghênh. Bạn có thể: - Tạo issue để báo lỗi
hoặc đề xuất cải tiến - Gửi pull request

------------------------------------------------------------------------

## Tác giả

-   Trần Huy Hậu
-   Lương Minh Nhật
-   Trần Minh Quân

------------------------------------------------------------------------

## Credits

Dự án sử dụng và tham khảo từ các nguồn:

-   ROS2 Navigation (Nav2)
-   Cartographer
-   robot_localization
-   Open Robotics
