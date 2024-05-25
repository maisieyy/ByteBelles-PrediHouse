// NAVBAR SCROLLED
const navEl = document.querySelector(".navbar");

window.addEventListener("scroll", () => {
  if (window.scrollY >= 56) {
    navEl.classList.add("navbar-scrolled");
  } else if (window.scrollY < 56) {
    navEl.classList.remove("navbar-scrolled");
  }
});

// REFRESH BUTTON

document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM terisi penih dan diuraikan");
  const formPredict = document.getElementById("form-predict");
  const refreshButton = document.getElementById("refreshButton");

  if (refreshButton) {
    console.log("Tombol refresh ditemukan");
    refreshButton.addEventListener("click", (event) => {
      event.preventDefault();
      console.log("Tombol refresh diklik");

      // reset form
      formPredict.reset();

      // menghapus semua input
      const inputs = formPredict.querySelectorAll("input[type='number']");
      inputs.forEach((input) => {
        input.value = "";
        console.log(`menghapus input dengan name: ${input.name}`);
      });

      // hapus bagian hasil dan rekomendasi
      const resultSection = document.querySelector(".result");
      const recomSection = document.querySelector(".recom-section");
      const recomResult = document.querySelector(".recom-result");

      if (resultSection) {
        resultSection.remove();
        console.log("Section hasil prediksi dihapus");
      }
      if (recomSection) {
        recomSection.remove();
        console.log("Section rekomendasi dihapus");
      }
      if (recomResult) {
        recomResult.remove();
        console.log("Section hasil rekomendasi dihapus");
      }

      // scroll ke form
      window.location.href = "#form-predict";
    });
  } else {
    console.log("Tombol refresh tidak ditemukan");
  }
});
