// Fonction appelée en cas de succès du scan
function onScanSuccess(decodedText, decodedResult) {
    document.getElementById('resultat').innerText = `Code scanné : ${decodedText}`;
    console.log("Résultat complet :", decodedResult);
  }

  // Fonction appelée en cas d'erreur
  function onScanError(errorMessage) {
    console.warn("Erreur de scan :", errorMessage);
  }

  // Initialisation du scanner
  let scanner = new Html5QrcodeScanner(
    "reader", { fps: 10, qrbox: 250 }
  );
  scanner.render(onScanSuccess, onScanError);