const date = new Date()
const time_options = {
    hour: "numeric",
    minute: "numeric",
}
const date_options = {
    weekday: "long",
    month: "long",
    day: 'numeric',
}
fa_time = date.toLocaleTimeString("fa-IR", time_options)
fa_date = date.toLocaleDateString("fa-IR", date_options)
final_date_time = fa_date + ' ' + fa_time
const time_header = document.getElementById('time-header').innerText = final_date_time