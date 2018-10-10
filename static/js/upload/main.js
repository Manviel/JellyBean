let result = document.querySelector('.result'),
  img_result = document.querySelector('.img-result'),
  save = document.querySelector('.save'),
  cropped = document.querySelector('.cropped'),
  upload = document.querySelector('#file-input'),
  cropper = '';

upload.addEventListener('change', (e) => {
  if (e.target.files.length) {
    const reader = new FileReader();

    reader.onload = (e) => {
      if (e.target.result) {
        let img = document.createElement('img');

        img.id = 'image';
        img.src = e.target.result

        result.innerHTML = '';
        result.appendChild(img);
        save.classList.remove('hide');

        cropper = new Cropper(img);
      }
    };
    reader.readAsDataURL(e.target.files[0]);
  }
});

save.addEventListener('click', (e) => {
  e.preventDefault();

  let imgSrc = cropper.getCroppedCanvas({width: 100, height: 100}).toDataURL();

  cropped.classList.remove('hide');
  img_result.classList.remove('hide');

  cropped.src = imgSrc;
});
