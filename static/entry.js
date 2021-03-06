
async function compelete() {
    let resp = await fetch('https://gsheet.moridisa.com/autofirebase/compelete_sheet');
    let resp_json = await resp.json()
    console.log(resp_json)
    var li = document.createElement("li");
    var i = document.createElement("i")
    li.setAttribute("class", "list-group-item")

    if (resp_json.status === "OK") {
        i.setAttribute("class", "bi-check-circle")
        li.textContent = "Done"
    }
    else {
        i.setAttribute("class", "bi-x-circle")
        li.textContent = "Failed"
    }
    li.appendChild(i)
    document.getElementById("translate_card_body").appendChild(li)
}

async function autofill() {
    let resp = await fetch('https://gsheet.moridisa.com/autofirebase/reading_sheet');
    let resp_json = await resp.json();
    console.log(resp_json)
};


async function inject_func(noti_list) {

    function sleep(time) {

        var basic_time = 1000
        if (time != null) {
            basic_time *= time
        }
        return new Promise((resolve) => setTimeout(resolve, basic_time));
    }

    for (let index = 0; index < noti_list.length; index++) {
        now = Date.now()
        var noti = noti_list[index];

        // create new noti
        await document.getElementsByClassName("newCampaign")[0].click()
        await sleep(0.8)

        // fill up noti content
        document.getElementsByClassName("message-title")[0].value = noti.title;
        document.getElementsByClassName("message-title")[0].dispatchEvent(new Event("input"));
        document.getElementsByClassName("message-text")[0].value = noti.desc;
        document.getElementsByClassName("message-text")[0].dispatchEvent(new Event("input"));
        document.getElementsByClassName("notification-image-input")[0].value = noti.pic;
        document.getElementsByClassName("notification-image-input")[0].dispatchEvent(new Event("input"));
        document.getElementsByClassName("message-label")[0].value = noti.name;
        document.getElementsByClassName("message-label")[0].dispatchEvent(new Event("input"));

        // next
        await sleep(0.8)
        document.getElementsByClassName("mat-stepper-next")[0].click()
        await sleep(1)

        // ????????????app
        console.log("????????????app")
        document.getElementsByClassName("mat-select-value")[1].click()
        await sleep(0.3)

        // ???????????????app
        console.log("???????????????app")
        document.getElementsByClassName("mat-option")[0].click()
        await sleep(0.3)

        // ?????????????????????
        console.log("?????????????????????")
        document.getElementsByClassName("and-button")[0].click()
        await sleep(0.3)

        // ??????????????????
        console.log("??????????????????")
        document.getElementsByTagName("fire-rx-targeting-options")[1].children[0].click()
        await sleep(0.3)

        // ??????????????????
        console.log("??????????????????")
        document.getElementsByClassName("mat-menu-item")[1].click()
        await sleep(0.3)

        // ??????????????????
        console.log("??????????????????")
        document.getElementsByClassName("mat-select-value")[3].click()
        await sleep(0.3)

        // ????????????
        var lans = document.getElementsByClassName("mat-option")
        for (let index = 0; index < lans.length; index++) {
            var lan = lans.item(index)
            var lan_text = lan.textContent.split(" ")[1];
            var flag = false;
            if (noti.lan.operation === 'in') {
                flag = noti.lan.lan_list.indexOf(lan_text) !== -1
            } else {
                flag = noti.lan.lan_list.indexOf(lan_text) === -1
            }
            if (flag) {
                lan.click()
                // await sleep(0.8)
            }
        }
        await sleep(0.3)
        // ????????????
        document.getElementsByClassName("cdk-overlay-backdrop")[0].click()
        await sleep(0.8)

        // ???????????????app
        document.getElementsByClassName("add-app")[0].click()
        await sleep(0.3)

        // ?????????????????????app
        console.log("?????????????????????app")
        document.getElementsByClassName("mat-select-value")[4].click()
        await sleep(0.3)

        // ???????????????app
        console.log("???????????????app")
        document.getElementsByClassName("mat-option")[0].click()
        await sleep(0.3)

        // ????????????????????????
        console.log("????????????????????????")
        document.getElementsByClassName("and-button")[2].click()
        await sleep(0.3)

        // ??????????????????????????????
        console.log("??????????????????????????????")
        document.getElementsByTagName("fire-rx-targeting-options")[3].children[0].click()
        await sleep(0.3)

        // ???????????????????????????
        console.log("???????????????????????????")
        document.getElementsByClassName("mat-menu-item")[1].click()
        await sleep(0.3)

        // ??????????????????
        console.log("??????????????????")
        document.getElementsByClassName("mat-select-value")[6].click()
        await sleep(0.3)

        // ????????????
        var lans = document.getElementsByClassName("mat-option")
        for (let index = 0; index < lans.length; index++) {
            var lan = lans.item(index)
            var lan_text = lan.textContent.split(" ")[1];
            var flag = false;
            if (noti.lan.operation === 'in') {
                flag = noti.lan.lan_list.indexOf(lan_text) !== -1
            } else {
                flag = noti.lan.lan_list.indexOf(lan_text) === -1
            }
            if (flag) {
                lan.click()
                // await sleep(0.8)
            }
        }
        // ????????????
        document.getElementsByClassName("cdk-overlay-backdrop")[0].click()
        await sleep(0.8)

        // next
        await sleep(0.8)
        document.getElementsByClassName("mat-stepper-next")[1].click()
        await sleep(1)

        // ??????????????????
        console.log("??????????????????")
        document.getElementsByTagName("fcm-datepicker")[0].getElementsByTagName("input")[0].click()
        await sleep(0.3)

        // ????????????
        console.log("????????????")
        document.getElementsByClassName("mat-menu-item")[1].click()
        await sleep(0.3)

        // ??????????????????
        console.log("??????????????????")
        document.getElementsByClassName("mat-calendar-period-button")[0].click()
        await sleep(0.3)

        // ??????
        console.log("??????")
        var calendar_year_cells = document.getElementsByClassName("mat-calendar-body-cell")
        for (let index = 0; index < calendar_year_cells.length; index++) {
            let calendar_year_cell = calendar_year_cells.item(index)
            if (calendar_year_cell.textContent.trim() === noti.push_date.year) {
                calendar_year_cell.click()
                break
            }
        }
        await sleep(0.3)

        // ??????
        console.log("??????")
        var calendar_month_cells = document.getElementsByClassName("mat-calendar-body-cell")
        for (let index = 0; index < calendar_month_cells.length; index++) {
            let calendar_month_cell = calendar_month_cells.item(index)
            if (calendar_month_cell.textContent.trim() === noti.push_date.month.str) {
                calendar_month_cell.click()
                break
            }
        }
        await sleep(0.3)

        // ??????
        console.log("??????")
        var calendar_day_cells = document.getElementsByClassName("mat-calendar-body-cell")
        for (let index = 0; index < calendar_day_cells.length; index++) {
            let calendar_day_cell = calendar_day_cells.item(index)
            if (calendar_day_cell.textContent.trim() === noti.push_date.day) {
                calendar_day_cell.click()
                break
            }
        }
        await sleep(0.3)

        // ????????????
        console.log("????????????")
        document.getElementsByTagName("fcm-datetimepicker")[0].getElementsByTagName("input")[1].value = `${noti.push_time.hour}:${noti.push_time.minute}`
        document.getElementsByTagName("fcm-datetimepicker")[0].getElementsByTagName("input")[1].dispatchEvent(new Event("input"))
        // await sleep(0.8)

        // ????????????
        console.log("????????????")
        document.getElementsByClassName("fcm-timezonepicker-button")[0].click()
        // await sleep(0.8)

        // ??????
        console.log("?????????")
        var btns = document.getElementsByClassName("mat-menu-item")
        for (let index = 0; index < btns.length; index++) {
            let btn = btns.item(index)
            if (btn.textContent === "Recipient time zone") {
                btn.click()
                break
            }
        }
        await sleep(0.3)

        // next
        document.getElementsByClassName("mat-stepper-next")[2].click()
        await sleep(0.8)

        document.getElementsByClassName("mat-stepper-next")[3].click()
        await sleep(0.8)

        // kv
        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[1].value = "push_from"
        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[1].dispatchEvent(new Event("input"));

        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[2].value = "FcmPush"
        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[2].dispatchEvent(new Event("input"));

        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[3].value = "notify_id"
        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[3].dispatchEvent(new Event("input"));

        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[4].value = `${noti.push_date.year}${noti.push_date.month.int}${noti.push_date.day}`
        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[4].dispatchEvent(new Event("input"));

        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[5].value = "notify_time"
        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[5].dispatchEvent(new Event("input"));

        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[6].value = `${noti.push_time.hour}${noti.push_time.minute}`
        document.getElementsByClassName("abt-message-options-form")[0].getElementsByTagName("input")[6].dispatchEvent(new Event("input"));
        await sleep(0.3)

        document.getElementsByClassName("mat-select-value")[7].click()
        await sleep(0.3)

        var options = document.getElementsByClassName("mat-option")
        for (let index = 0; index < options.length; index++) {
            let option = options.item(index)
            if (option.textContent.trim() == 'Enabled') {
                option.click()
                break
            }
        }
        await sleep(0.3)

        document.getElementsByClassName("mat-select-value")[8].click()
        await sleep(0.3)

        var options = document.getElementsByClassName("mat-option")
        for (let index = 0; index < options.length; index++) {
            let option = options.item(index)
            if (option.textContent.trim() == 'Enabled') {
                option.click()
                break
            }
        }
        await sleep(0.3)

        document.getElementsByClassName("badge-count-input")[0].value = 1
        document.getElementsByClassName("badge-count-input")[0].dispatchEvent(new Event("input"))
        // await sleep(0.8)

        document.getElementsByClassName("cta-bottom")[0].getElementsByTagName("button")[1].click()
        await sleep(0.3)

        document.getElementsByClassName("fire-dialog-actions")[0].getElementsByTagName("button")[1].click()
        console.log(`?????????: ${index + 1}??? not???????????????, ??????: ${noti_list.length - 1 - index}???, ??????: ${Date.now() - now}ms, 10s??????????????????`)
        await sleep(10)
    }
    alert("Shift Bro, ?????????");

}

let compeleteBtn = document.getElementById("compelete");
let autofillBtn = document.getElementById("autofill");

compeleteBtn.addEventListener("click", compelete);
autofillBtn.addEventListener("click", autofill);
