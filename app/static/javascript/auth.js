forgotPassword = () => {
  console.log('You forgot the password :p')
}

$(document).ready(() => {
  let url = new URL(window.location.href);
  let next = url.searchParams.get("next");
  // Todo: Send this next to the server with the 
  // login form in order to properly redirect.
});