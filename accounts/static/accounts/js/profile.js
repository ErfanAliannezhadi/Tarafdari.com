if (is_owner === false) {

    const follow_button = document.getElementsByClassName('follow-button')[0]
    follow_button.addEventListener('click', function () {
        if (is_followed === true) {
            console.log('unfollow process...')
            const unfollow_ajax_request = new XMLHttpRequest()
            unfollow_ajax_request.onload = function () {
                let response = JSON.parse(this.response).response
                if (response === 'it was not followed') {
                    alert('شما این کاربر را قبلا دنبال نکرده اید')
                }
                if (response === 'it is unfollowed') {
                    follow_button.innerHTML = '<i class="follow-icon"></i>دنبال کن '
                    is_followed = false
                }
            }
            unfollow_ajax_request.open('GET', unfollow_url)
            unfollow_ajax_request.send()
        } else {
            console.log('follow process')
            const follow_ajax_request = new XMLHttpRequest()
            follow_ajax_request.onload = function () {
                let response = JSON.parse(this.response).response
                if (response === 'it was followed') {
                    alert('شما این کاربر را قبلا دنبال کرده اید')
                }
                if (response === 'it is followed') {
                    follow_button.innerHTML = '<i class="follow-icon"></i> توقف دنبال کردن '
                    is_followed = true
                }
            }
            follow_ajax_request.open('GET', follow_url)
            follow_ajax_request.send()
        }
    })
}

