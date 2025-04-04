  const fileInput = document.getElementById('file-upload');
  const fileNameDisplay = document.getElementById('file-name');

  fileInput.addEventListener('change', function() {
    if (this.files.length > 0) {
      fileNameDisplay.textContent = this.files[0].name;
    } else {
      fileNameDisplay.textContent = 'No file selected';
    }
  });

  const searchInput = document.getElementById('file-search');
  const fileItems = document.querySelectorAll('ul li');

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();

    fileItems.forEach(item => {
      const fileName = item.querySelector('a').textContent.toLowerCase();
      item.style.display = fileName.includes(query) ? 'flex' : 'none';
    });
  });

  const sortSelect = document.getElementById('sort-select');
  const fileList = document.querySelector('ul');
  const sortableItems = Array.from(fileList.children);

  sortSelect.addEventListener('change', () => {
    const direction = sortSelect.value;

    const sorted = sortableItems
      .slice()
      .sort((a, b) => {
        const nameA = a.querySelector('a').textContent.toLowerCase();
        const nameB = b.querySelector('a').textContent.toLowerCase();

        if (direction === 'az') {
          return nameA.localeCompare(nameB);
        } else {
          return nameB.localeCompare(nameA);
        }
      });

    fileList.innerHTML = '';
    sorted.forEach(item => fileList.appendChild(item));
  });

