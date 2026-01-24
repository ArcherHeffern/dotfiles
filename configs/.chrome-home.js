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