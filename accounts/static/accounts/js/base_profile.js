if (is_owner === false) {

    const follow_button = document.getElementsByClassName('follow-button')[0]
    follow_button.addEventListener('click', function () {
        if (is_followed === true || is_follow_requested === true) {

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
                if (response === 'it is unfollow requested') {
                    follow_button.innerHTML = '<i class="follow-icon"></i>درخواست فالو '
                    is_follow_requested = false
                }
            }
            unfollow_ajax_request.open('GET', unfollow_url)
            unfollow_ajax_request.send()
        } else {
            const follow_ajax_request = new XMLHttpRequest()
            follow_ajax_request.onload = function () {
                let response = JSON.parse(this.response).response
                if (response === 'it was followed') {
                    alert('شما این کاربر را قبلا دنبال کرده اید')
                }
                if (response === 'it was follow requested') {
                    alert('شما قبلا درخواست فالو به این کاربر داده اید')
                }
                if (response === 'it is followed') {
                    follow_button.innerHTML = '<i class="follow-icon"></i> توقف دنبال کردن '
                    is_followed = true
                }
                if (response === 'it is follow requested') {
                    follow_button.innerHTML = '<i class="follow-icon"></i> حذف درخواست '
                    is_follow_requested = true
                }
            }
            follow_ajax_request.open('GET', follow_url)
            follow_ajax_request.send()
        }
    })
}

function emoji_reverse(name) {
    function ajax_request(event) {
        event.preventDefault();
        const emoji_ajax_request = new XMLHttpRequest()
        emoji_ajax_request.onload = function () {
            let response = JSON.parse(this.response).response
            if (response === 'done') {
                if (name === 'heart') {
                    if (selected_heart) {
                        emoji_heart.className = 'emoji-heart'
                        emoji_heart.innerHTML = (parseInt(emoji_heart.innerHTML) - 1).toString()
                        selected_heart = false
                    } else {
                        emoji_heart.className = 'emoji-heart selected'
                        emoji_heart.innerHTML = (parseInt(emoji_heart.innerHTML) + 1).toString()
                        selected_heart = true
                    }
                }
                if (name === 'trophy') {
                    if (selected_trophy) {
                        emoji_trophy.className = 'emoji-trophy'
                        emoji_trophy.innerHTML = (parseInt(emoji_trophy.innerHTML) - 1).toString()
                        selected_trophy = false
                    } else {
                        emoji_trophy.className = 'emoji-trophy selected'
                        emoji_trophy.innerHTML = (parseInt(emoji_trophy.innerHTML) + 1).toString()

                        selected_trophy = true
                    }
                }
                if (name === 'passion') {
                    if (selected_passion) {
                        emoji_passion.className = 'emoji-passion'
                        emoji_passion.innerHTML = (parseInt(emoji_passion.innerHTML) - 1).toString()
                        selected_passion = false
                    } else {
                        emoji_passion.className = 'emoji-passion selected'
                        emoji_passion.innerHTML = (parseInt(emoji_passion.innerHTML) + 1).toString()
                        selected_passion = true
                    }
                }
            } else {
                alert('این درخواست غیرقابل اجرا است')
            }
        }
        emoji_ajax_request.open('GET', `${reverse_emoji_url}?emoji=${name}`)
        emoji_ajax_request.send()
    }

    return ajax_request
}

const emoji_heart = document.getElementsByClassName('emoji-heart')[0]
const emoji_trophy = document.getElementsByClassName('emoji-trophy')[0]
const emoji_passion = document.getElementsByClassName('emoji-passion')[0]
emoji_heart.addEventListener('click', emoji_reverse('heart'))
emoji_trophy.addEventListener('click', emoji_reverse('trophy'))
emoji_passion.addEventListener('click', emoji_reverse('passion'))

const add_post = document.querySelector('#add-post h2')
const block_post = document.querySelector('#add-post div')
add_post.addEventListener('click', function (e) {
    e.preventDefault()
    if (block_post.style.display === 'block') {
        block_post.style.display = 'none'
    } else {
        block_post.style.display = 'block'
    }
})