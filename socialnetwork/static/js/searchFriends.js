const searchForm = document.getElementById('search_form');
const searchInput = document.getElementById('search_input');
const resultsBox = document.getElementById('box_results');
const resultFriendsBox = document.querySelector('.friends_list');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;


const sendSearchFriends = (friend) => {
  $.ajax({
      type: 'POST',
      url: 'search_friend',
      data: {
        'csrfmiddlewaretoken': csrf,
        'friend': friend,
      },

      success: (res) => {
        resultsBox.style.display = 'block';
        resultFriendsBox.style.display = 'none';
        console.log(res.data);
        const data = res.data;

        if (Array.isArray(data)) {
          resultsBox.innerHTML = ""
          data.forEach(friend => {
            resultsBox.innerHTML += `
                    <div class="card-body shadow-sm holder-bottom">
                      <div class="row">
                        <div class="col-2">
                          <img src="${ friend.avatar }" class="rounded mx-auto d-block mb-2" width="70" height="70">
                        </div>
                        <div class="col-4">
                          <p class="fs-5 mb-2">${ friend.first_name } ${ friend.last_name }</p>
                          <p class="text-muted fw-light">${ friend.bio }</p>
                        </div>
                        <div class="col-3 col align-self-center d-grid gap-2">
                          <button class="btn btn-outline-primary" type="submit">See profile</button>
                        </div>
                        <div class="col-3 col align-self-center d-grid gap-2">
                          <button class="btn btn-outline-danger" type="submit">Remove from friends</button>
                        </div>
                      </div>
                    </div>
            `
          });
        } else {
            if (searchInput.value.length == 0) {
                resultsBox.style.display = 'none';
                resultFriendsBox.style.display = 'block';
            } else {
                resultsBox.innerHTML = `${data}`;
            }
        }
      },

      error: (err) => {
        console.log(err)
      }
  });
}


searchInput.addEventListener('keyup', (e)=> {
  console.log(e.target.value)
  sendSearchFriends(e.target.value)
})