import qrcode
import os

class QRCodeGenerator:
    def __init__(self):
        self.output_directory = "/home/moses/Downloads"

    def generate_qr_code(self, student_details, filename):

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

       
        qr.add_data(student_details)
        qr.make(fit=True)

    
        qr_img = qr.make_image(fill_color="black", back_color="white")

       
        file_path = os.path.join(self.output_directory, filename)
        qr_img.save(file_path)
        print(f"QR code generated and saved as {file_path}")

    def check_access(self, student_id):
        # Check if access should be granted based on student ID
        allowed_students = {
            "123456": ("John Doe", "Access Allowed"),
            "789012": ("Jane Smith", "Access Denied"),
            "345678": ("Alice Johnson", "Access Allowed")
        }
        if student_id in allowed_students:
            student_name, access_message = allowed_students[student_id]
            print(f"Access granted for {student_name}.")
            return access_message
        else:
            print(f"Access denied for Student ID: {student_id}. Hostel access is denied.")
            return None

    def download_all_qr_codes(self):
       
        for filename in os.listdir(self.output_directory):
            if filename.endswith(".png"):
                try:
                    os.rename(os.path.join(self.output_directory, filename),
                              os.path.join(self.output_directory, f"downloaded_{filename}"))
                    print(f"QR code {filename} downloaded.")
                except Exception as e:
                    print(f"Failed to download QR code {filename}: {e}")

def main():
    generator = QRCodeGenerator()

    students = [
        {"name": "John Doe", "id": "123456"},
        {"name": "Jane Smith", "id": "789012"},
        {"name": "Alice Johnson", "id": "345678"}
    ]

    for student in students:
        student_details = f"Student Name: {student['name']}\nID Number: {student['id']}"
        filename = f"student_qr_{student['id']}.png"  # Unique filename based on student ID
        
        access_message = generator.check_access(student['id'])
        if access_message:
            student_details += f"\n{access_message}"
        
        generator.generate_qr_code(student_details, filename)

    generator.download_all_qr_codes()

if __name__ == "__main__":
    main()