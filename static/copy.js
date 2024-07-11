async function copy(metar) {
    try {
      await navigator.clipboard.writeText(metar);
    } catch (error) {
      console.error(error.message);
    }
}