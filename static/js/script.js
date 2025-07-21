document.getElementById('searchForm').addEventListener('submit', function(e) { 
    e.preventDefault();
    
    const nama = document.getElementById('namaInput').value.trim();
    const loadingEl = document.getElementById('loading');
    const hasilEl = document.getElementById('hasil');
    const searchBtn = document.getElementById('searchBtn');
    
    if (!nama) {
        hasilEl.innerHTML = '<div class="error">❌ Nama tidak boleh kosong!</div>';
        return;
    }
    
    // tampilkan loading
    loadingEl.style.display = 'block';
    hasilEl.innerHTML = '';
    searchBtn.disabled = true;
    searchBtn.textContent = 'Mencari...';
    
    const formData = new FormData();
    formData.append('nama', nama);
    
    fetch('/cari', {
        method: 'POST',
        body: formData
    })
    .then(resp => resp.json())
    .then(data => {
        loadingEl.style.display = 'none';
        searchBtn.disabled = false;
        searchBtn.textContent = 'Cari';
        
        if (data.error) {
            hasilEl.innerHTML = `<div class="error">❌ ${data.error}</div>`;
        } else {
            displayResults(data.hasil);
        }
    })
    .catch(err => {
        loadingEl.style.display = 'none';
        searchBtn.disabled = false;
        searchBtn.textContent = 'Cari';
        hasilEl.innerHTML = '<div class="error">❌ Terjadi kesalahan saat mencari data.</div>';
        console.error('Error:', err);
    });
});

function displayResults(results) {
    const hasilEl = document.getElementById('hasil');
    let html = '';
    
    if (results.length > 1) {
        html += '<div class="multiple-results">📋 Ditemukan beberapa hasil, diurutkan berdasarkan kecocokan:</div>';
    }
    
    results.forEach((item, index) => {
        // Set ikon absen
        const isAbsen = (item.absen === "true" || item.absen === true);
        const absenIcon = isAbsen ? '✅ Hadir' : '❌ Tidak hadir';
        
        // Buat list kegiatan
        let kegiatanList = '<ul>';
        item.kegiatan.forEach(keg => {
            kegiatanList += `<li> ${keg}</li>`;
        });
        kegiatanList += '</ul>';
        
        html += `
            <div class="result-item">
                <h3>👤 ${item.nama_lengkap}</h3>
                <p>🏫 Kelas: ${item.kelas}</p>
                <p>🗒️ Kegiatan:</p>
                ${kegiatanList}
                <p class="status-absen">🕒 Status Absen: ${absenIcon}</p>
                <div class="checkbox-container">
                    <input type="checkbox" 
                           id="absen_${index}" 
                           ${isAbsen ? 'checked disabled' : ''} 
                           onchange="updateAbsen('${item.nama_lengkap}', this.checked, this)">
                    <label for="absen_${index}">
                        ${isAbsen ? 'Sudah diabsen' : 'Tandai hadir'}
                    </label>
                </div>
            </div>
        `;
    });
    
    hasilEl.innerHTML = html;
}

function updateAbsen(namaLengkap, isChecked, checkboxElement) {
    if (!isChecked) return; // Hanya proses jika checkbox dicentang
    
    const formData = new FormData();
    formData.append('nama', namaLengkap);
    formData.append('absen', 'true');
    
    // Debug: log request yang akan dikirim
    console.log('Sending request to /update_absen with:', {
        nama: namaLengkap,
        absen: 'true'
    });
    
    fetch('/update_absen', {
        method: 'POST',
        body: formData
    })
    .then(resp => {
        console.log('Response status:', resp.status);
        console.log('Response ok:', resp.ok);
        
        // Cek apakah response adalah JSON yang valid
        if (!resp.ok) {
            throw new Error(`HTTP error! status: ${resp.status}`);
        }
        
        return resp.json();
    })
    .then(data => {
        console.log('Response data:', data);
        
        if (data.success) {
            // Refresh tampilan untuk menunjukkan status terbaru
            const label = checkboxElement.nextElementSibling;
            checkboxElement.disabled = true;
            label.textContent = 'Sudah diabsen';
            
            // Update status absen di tampilan menggunakan class selector yang lebih spesifik
            const resultItem = checkboxElement.closest('.result-item');
            const statusText = resultItem.querySelector('.status-absen');
            
            if (statusText) {
                statusText.innerHTML = '🕒 Status Absen: ✅ Hadir';
            }
            
            alert(`✅ ${namaLengkap} berhasil diabsen!`);
        } else {
            console.error('Server returned success=false:', data);
            alert(`❌ Gagal mengupdate absen: ${data.error || 'Unknown error'}`);
            // Uncheck checkbox jika gagal
            checkboxElement.checked = false;
        }
    })
    .catch(err => {
        console.error('Fetch error details:', err);
        alert('❌ Terjadi kesalahan saat mengupdate absen. Cek console untuk detail.');
        // Uncheck checkbox jika gagal
        checkboxElement.checked = false;
    });
}

// Fokus pada input saat load
document.getElementById('namaInput').focus();

// Support tekan Enter di input
document.getElementById('namaInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('searchForm').dispatchEvent(new Event('submit'));
    }
});