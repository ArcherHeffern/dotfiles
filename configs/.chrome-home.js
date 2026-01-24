const data = [
    {
        "train": "1",
        "logo_color_hex": "#DC4D49",
        "street": "96th",
        "status": "Leave now",
    },
    {
        "train": "Q",
        "logo_color_hex": "f7d448",
        "street": "42nd",
        "status": "5 minutes",
    },
    {
        "train": "2",
        "logo_color_hex": "#DC4D49",
        "street": "96th",
        "status": "Last chance",
    },
]

const train_times_container = document.getElementById("train_times_container");

function createTrainTimeElement(train, logo_color_hex, street, status) {
    const container = document.createElement("div")
    /*
    <div id="train-times-container"
        style="display: flex; flex-direction: row; flex-wrap: nowrap; justify-content: space-around; width: 200px; border: 1px solid black; padding: 5px; align-items: center">
        <div class="left-group"
            style="display: flex; flex-direction: row; justify-content: flex-start; align-items: center">
            <div class="circle"
                style="border-radius: 50%; display: grid; place-items: center; ;background-color: red; font-weight: 700; width: 28px; height: 28px; margin-right: 10px;">
                1
            </div>
            <div>96th</div>
        </div>
        <div>
            Leave now
        </div>
    </div>
    */

}

function render(data) {
    train_times_container.innerHTML = "";
    array.forEach(element => {
        const train = element["train"]
        const logo_color_hex = element["logo_color_hex"]
        const street = element["street"]
        const status = element["status"]

        if (!train || !logo_color_hex || !street || !status) {
            console.error("Missing data when attempting to render")
            console.error(`${train}:${logo_color_hex}:${street}:${status}`)
        }

        train_times_container.appendChild(createTrainTimeElement(
            train, logo_color_hex, street, status
        ))

    });


}