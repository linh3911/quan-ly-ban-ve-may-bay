import java.util.ArrayList;
import java.util.Scanner;
import javax.swing.JOptionPane;
import javax.swing.table.DefaultTableModel;

// ==========================================
// 1. CLASS ĐỐI TƯỢNG HỌC SINH
// ==========================================
class HocSinh {
    private String maHS, hoTen, lop, queQuan;
    private int tuoi;

    public HocSinh(String maHS, String hoTen, int tuoi, String lop, String queQuan) {
        this.maHS = maHS;
        this.hoTen = hoTen;
        this.tuoi = tuoi;
        this.lop = lop;
        this.queQuan = queQuan;
    }

    public String getMaHS() {
        return maHS;
    }

    public String getHoTen() {
        return hoTen;
    }

    public int getTuoi() {
        return tuoi;
    }

    public String getLop() {
        return lop;
    }

    public String getQueQuan() {
        return queQuan;
    }

    public void setHoTen(String hoTen) {
        this.hoTen = hoTen;
    }

    public void setTuoi(int tuoi) {
        this.tuoi = tuoi;
    }

    public void setLop(String lop) {
        this.lop = lop;
    }

    public void setQueQuan(String queQuan) {
        this.queQuan = queQuan;
    }
}

// ==========================================
// 2. CLASS CHÍNH - GIAO DIỆN VÀ XỬ LÝ LÔGIC
// ==========================================
public class CuoiKy2026 extends javax.swing.JFrame {

    private static ArrayList<HocSinh> danhSachHS = new ArrayList<>();
    private DefaultTableModel tableModel;

    private javax.swing.JTextField txtMaHS, txtHoTen, txtTuoi, txtLop, txtQueQuan;
    private javax.swing.JButton btnThem, btnSua, btnXoa, btnCapNhat, btnLamMoi;
    private javax.swing.JTable tblHocSinh;

    public CuoiKy2026() {
        initComponentsManual();
        tableModel = (DefaultTableModel) tblHocSinh.getModel();
        btnCapNhat.setEnabled(false);
        setLocationRelativeTo(null);
        hienThi();
    }

    private void initComponentsManual() {
        setTitle("CHUONG TRINH QUAN LY HOC SINH - 2026");
        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLayout(new java.awt.BorderLayout(10, 10));

        javax.swing.JPanel pnlInput = new javax.swing.JPanel(new java.awt.GridLayout(5, 2, 10, 10));
        pnlInput.setBorder(javax.swing.BorderFactory.createEmptyBorder(15, 15, 15, 15));

        pnlInput.add(new javax.swing.JLabel("Ma Hoc Sinh:"));
        txtMaHS = new javax.swing.JTextField();
        pnlInput.add(txtMaHS);
        pnlInput.add(new javax.swing.JLabel("Ho va Ten:"));
        txtHoTen = new javax.swing.JTextField();
        pnlInput.add(txtHoTen);
        pnlInput.add(new javax.swing.JLabel("Tuoi:"));
        txtTuoi = new javax.swing.JTextField();
        pnlInput.add(txtTuoi);
        pnlInput.add(new javax.swing.JLabel("Lop:"));
        txtLop = new javax.swing.JTextField();
        pnlInput.add(txtLop);
        pnlInput.add(new javax.swing.JLabel("Que Quan:"));
        txtQueQuan = new javax.swing.JTextField();
        pnlInput.add(txtQueQuan);

        javax.swing.JPanel pnlButtons = new javax.swing.JPanel(
                new java.awt.FlowLayout(java.awt.FlowLayout.CENTER, 15, 10));
        btnThem = new javax.swing.JButton("Them Moi");
        btnSua = new javax.swing.JButton("Chon Sua");
        btnXoa = new javax.swing.JButton("Xoa Bo");
        btnCapNhat = new javax.swing.JButton("Cap Nhat");
        btnLamMoi = new javax.swing.JButton("Lam Moi");

        pnlButtons.add(btnThem);
        pnlButtons.add(btnSua);
        pnlButtons.add(btnXoa);
        pnlButtons.add(btnCapNhat);
        pnlButtons.add(btnLamMoi);

        javax.swing.JPanel pnlTop = new javax.swing.JPanel(new java.awt.BorderLayout());
        pnlTop.add(pnlInput, java.awt.BorderLayout.CENTER);
        pnlTop.add(pnlButtons, java.awt.BorderLayout.SOUTH);
        add(pnlTop, java.awt.BorderLayout.NORTH);

        String[] columnNames = { "Ma HS", "Ho va Ten", "Tuoi", "Lop", "Que Quan" };
        DefaultTableModel model = new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int r, int c) {
                return false;
            }
        };
        tblHocSinh = new javax.swing.JTable(model);
        javax.swing.JScrollPane scrollPane = new javax.swing.JScrollPane(tblHocSinh);
        add(scrollPane, java.awt.BorderLayout.CENTER);

        // ĐĂNG KÝ SỰ KIỆN NÚT BẤM CHUẨN XÁC
        btnThem.addActionListener(e -> themHS());
        btnSua.addActionListener(e -> suaHS());
        btnCapNhat.addActionListener(e -> capNhatHS());
        btnXoa.addActionListener(e -> xoaHS());
        btnLamMoi.addActionListener(e -> lamMoiForm()); // Gọi đúng hàm làm mới form
    }

    private void hienThi() {
        if (tableModel != null) {
            tableModel.setRowCount(0);
            for (HocSinh hs : danhSachHS) {
                Object[] row = { hs.getMaHS(), hs.getHoTen(), hs.getTuoi(), hs.getLop(), hs.getQueQuan() };
                tableModel.addRow(row);
            }
        }
    }

    // SỬA ĐỔI TRIỆT ĐỂ: ÉP BUỘC XÓA TRẮNG CHỮ VÀ PHỤC HỒI TRẠNG THÁI KHÓA/MỞ
    private void lamMoiForm() {
        txtMaHS.setText("");
        txtHoTen.setText("");
        txtTuoi.setText("");
        txtLop.setText("");
        txtQueQuan.setText("");

        txtMaHS.setEditable(true); // Mở khóa lại ô Mã học sinh
        btnThem.setEnabled(true); // Sáng lại nút Thêm Mới
        btnCapNhat.setEnabled(false); // Tắt nút Cập Nhật đi
    }

    private void themHS() {
        String ma = txtMaHS.getText().trim();
        String ten = txtHoTen.getText().trim();
        String lop = txtLop.getText().trim();
        String que = txtQueQuan.getText().trim();
        if (ma.isEmpty() || ten.isEmpty() || lop.isEmpty() || que.isEmpty() || txtTuoi.getText().isEmpty()) {
            JOptionPane.showMessageDialog(this, "Vui long nhap du thong tin!");
            return;
        }
        int tuoi;
        try {
            tuoi = Integer.parseInt(txtTuoi.getText().trim());
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(this, "Tuoi phai la so!");
            return;
        }

        danhSachHS.add(new HocSinh(ma, ten, tuoi, lop, que));
        hienThi();
        lamMoiForm();
        JOptionPane.showMessageDialog(this, "Them thanh cong!");
    }

    private void suaHS() {
        int row = tblHocSinh.getSelectedRow();
        if (row == -1) {
            JOptionPane.showMessageDialog(this, "Chon 1 dong de sua!");
            return;
        }
        txtMaHS.setText(tableModel.getValueAt(row, 0).toString());
        txtHoTen.setText(tableModel.getValueAt(row, 1).toString());
        txtTuoi.setText(tableModel.getValueAt(row, 2).toString());
        txtLop.setText(tableModel.getValueAt(row, 3).toString());
        txtQueQuan.setText(tableModel.getValueAt(row, 4).toString());

        txtMaHS.setEditable(false); // Khóa ô Mã học sinh lại khi sửa
        btnCapNhat.setEnabled(true); // Bật nút Cập Nhật lên
        btnThem.setEnabled(false); // Tắt nút Thêm Mới đi
    }

    private void capNhatHS() {
        String ma = txtMaHS.getText().trim();
        String ten = txtHoTen.getText().trim();
        String lop = txtLop.getText().trim();
        String que = txtQueQuan.getText().trim();
        int tuoi = Integer.parseInt(txtTuoi.getText().trim());
        for (HocSinh hs : danhSachHS) {
            if (hs.getMaHS().equalsIgnoreCase(ma)) {
                hs.setHoTen(ten);
                hs.setTuoi(tuoi);
                hs.setLop(lop);
                hs.setQueQuan(que);
                break;
            }
        }
        hienThi();
        lamMoiForm();
        JOptionPane.showMessageDialog(this, "Cap nhat thanh cong!");
    }

    private void xoaHS() {
        int row = tblHocSinh.getSelectedRow();
        if (row == -1) {
            JOptionPane.showMessageDialog(this, "Chon dong can xoa!");
            return;
        }
        String ma = tableModel.getValueAt(row, 0).toString();
        for (int i = 0; i < danhSachHS.size(); i++) {
            if (danhSachHS.get(i).getMaHS().equalsIgnoreCase(ma)) {
                danhSachHS.remove(i);
                break;
            }
        }
        hienThi();
        lamMoiForm();
    }

    public static void gioiThieuVaPhanLoai() {
        Scanner banPhim = new Scanner(System.in);
        int soThuTu = 1;

        System.out.println("====== CHUONG TRINH NHAP THONG TIN CA NHAN ======");

        while (true) {
            System.out.println("\n--- Nhap thong tin hoc sinh thu " + soThuTu + " ---");
            System.out.print("Moi ban nhap Ho va Ten: ");
            String hoTen = banPhim.nextLine();

            System.out.print("Moi ban nhap Lop hoc: ");
            String lopHoc = banPhim.nextLine();

            System.out.print("Moi ban nhap Que quan: ");
            String queQuan = banPhim.nextLine();

            System.out.print("Moi ban nhap Tuoi: ");
            int tuoi = banPhim.nextInt();
            banPhim.nextLine();

            if (tuoi <= 0) {
                System.out.println("[LOI]: So tuoi khong hop le! Vui long nhap lai hoc sinh nay.");
                continue;
            }

            String maTuDong = "BP_" + soThuTu;
            danhSachHS.add(new HocSinh(maTuDong, hoTen, tuoi, lopHoc, queQuan));
            System.out.println("=> Da luu tam hoc sinh " + hoTen + " vao hang doi!");

            System.out.print(
                    "\nBan co muon nhap tiep hoc sinh khac khong? (Bam Y de tiep tuc / Bam phim bat ky de mo Giao dien): ");
            String luaChon = banPhim.nextLine().trim();
            if (!luaChon.equalsIgnoreCase("Y")) {
                break;
            }
            soThuTu++;
        }

        System.out.println("\n------------------------------------------------");
        System.out.println("-> Hoan tat nhap tu ban phim! Dang mo cua so giao dien...");
        System.out.println("------------------------------------------------");
    }

    public static void main(String args[]) {
        gioiThieuVaPhanLoai();
        java.awt.EventQueue.invokeLater(() -> {
            new CuoiKy2026().setVisible(true);
        });
    }
}