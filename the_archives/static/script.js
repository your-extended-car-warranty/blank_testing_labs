/*
Brian Balderas-Ortega, Tyler Khin
script.js
April 17th, 2025

Contains the scripts for the book tracker
*/

function markAsRead(bookId) {
    fetch(`/mark-read/${bookId}`, {
      method: "POST",
    })
    .then(res => res.json())
    .then(data => {
      if (data.status === "success") {
        // Reload the page or modify DOM
        reloadPage();
      } else {
        alert("Failed to mark book as read.");
      }
    });
  }

function deleteBook(bookId) {
    fetch(`/delete/${bookId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const row = document.getElementById(`book-${bookId}`);
            row.remove();
            reloadPage();
        }
    });
}

function editBook(bookId) {
    window.location.href = `/edit/${bookId}`;
}

function viewBook(bookId) {
    window.location.href = `/view/${bookId}`;
}

function addBook() {
    window.location.href = `/add`;
}

async function searchGoogleBooks() {
    // call API
    const query = document.getElementById('searchQuery').value;
    const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
    const results = await res.json();
  
    const container = document.getElementById('searchResults');
    container.innerHTML = '';

    results.forEach(book => {
        const div = document.createElement('div');
        div.innerHTML = `
          <div style="display:flex; gap: 1rem; align-items:center;">
            <img src="${book.image}" alt="Cover" height="100">
            <div>
              <strong>${book.title}</strong> by ${book.author}<br>
              <em>${book.genre || 'Genre Not Listed'}</em><br>
              <em>${book.rating || '--'}/5 from ${book.ratingsCount || '0'} review(s)</em><br>
              <button 
                class="use-book"
                data-title="${book.title || ''}"
                data-author="${book.author || ''}"
                data-genre="${book.genre || ''}"
                data-notes="${book.description || ''}"
                data-rating="${book.rating || ''}"
                data-image="${book.image || ''}"
              >Use this</button>
            </div>
          </div>
          <hr>
        `;
        container.appendChild(div);
      });

      document.addEventListener("click", function (e) {
        if (e.target.classList.contains("use-book")) {
          const btn = e.target;
          document.getElementById("title").value = btn.dataset.title;
          document.getElementById("author").value = btn.dataset.author;
          document.getElementById("genre").value = btn.dataset.genre;
          document.getElementById("notes").value = btn.dataset.notes;
          document.getElementById("rating").value = btn.dataset.rating;
          document.getElementById("addBookForm").submit();
        }
      });
    }
  
function reloadPage() {
    location.reload();
}