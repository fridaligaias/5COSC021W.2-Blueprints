document.addEventListener('DOMContentLoaded', function() {
  // Lấy tất cả các role card
  const roleCards = document.querySelectorAll('.role-card');
  const hiddenRoleInput = document.getElementById('selected-role');
  
  // Thêm sự kiện click cho mỗi role card
  roleCards.forEach(card => {
      card.addEventListener('click', function() {
          // Loại bỏ class active khỏi tất cả các role card
          roleCards.forEach(c => {
              c.querySelector('.role-icon').classList.remove('active');
          });
          
          // Thêm class active cho role card được chọn
          this.querySelector('.role-icon').classList.add('active');
          
          // Cập nhật giá trị hidden input
          hiddenRoleInput.value = this.getAttribute('data-role');
      });
  });
});