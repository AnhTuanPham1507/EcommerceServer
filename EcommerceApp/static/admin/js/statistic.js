var data = $('#my-user').data()

const getRevenues = async () => {
    const response = await fetch("http://127.0.0.1:8000/revenue/get-revenue/", {
        mode: 'cors',
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({"username": data.name, "password": data.other})
    })

    if (response.status === 202) {
        const revenues = await response.json()
        let objRevenues = {}
        revenues.forEach(element => {
            const created_date = new Date(element['created_date'])
            const year = created_date.getFullYear()
            const month = created_date.getMonth() + 1
            if (objRevenues.hasOwnProperty(year))

                if (objRevenues[year].hasOwnProperty(month))
                    objRevenues[year][month] += element['ecommerce_income']
                else
                    objRevenues[year] = { ...objRevenues[year], ...{ [month]: element['ecommerce_income'] } }

            else
                objRevenues[year] = { [month]: element['ecommerce_income'] }
        })

        return objRevenues
    }
    else{
        return undefined
    }

}

const addValToCombo = () => {
    utils('get_years')
        .then(func => func())
        .then(years => {
            const selectYear = document.getElementById('choosedYear')
            years.forEach(year => {
                selectYear.innerHTML += `<option value=${year}>${year}</option>`
            })
        })
        .catch(err => {
            console.log(err)
        })

}

const renderChar = (choosedType, choosedYear) => {
    utils('get_value')
        .then(func => func(choosedYear))
        .then(({ months, incomes }) => {
            const labels = months
            const data = {
                labels: labels,
                datasets: [{
                    label: `stats for ${choosedYear}`,
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: incomes,
                }]
            };

            const config = {
                type: choosedType,
                data: data,
                options: {
                }
            };

            const chart = new Chart(
                document.getElementById('myChart'),
                config
            );
        })
        .catch(err => {
            console.log(err)
        })
}


function updateChart(choosedYear, choosedType) {
    utils('get_value')
        .then(func => func(choosedYear))
        .then(({ months, incomes }) => {
            let chart = {}
            Chart.helpers.each(Chart.instances, function (instance) {
                chart = instance
            })
            chart.data.labels = months;
            chart.data.datasets.forEach((dataset) => {
                dataset.label = choosedYear
                dataset.data = incomes
            });

            chart.update();
        })
        .catch(err => {
            console.log(err)
        })

}

const utils = async (choosedFunc) => {
    const objRevenues = await getRevenues()

    if (choosedFunc === "get_years")
        return () => {
            const years = []
            for (const year in objRevenues)
                years.push(year)
            return Promise.resolve(years)
        }

    if (choosedFunc === 'get_value')
        return (year) => {
            const months = []
            const incomes = []
            for (const month in objRevenues[year]) {
                console.log(month)
                months.push(month)
                incomes.push(objRevenues[year][month])
            }
            return Promise.resolve({ months, incomes })
        }

}

document.getElementById('choosedYear').addEventListener('change', (e) => {
    const year = parseInt(e.target.value)
    const type = $('#choosedType').val()
    updateChart(year, type)
})

document.getElementById('choosedType').addEventListener('change', (e) => {
    const year = parseInt($('#choosedYear').val())
    const type = e.target.value
    Chart.helpers.each(Chart.instances, function (instance) {
        instance.destroy()
    })
    renderChar(type, year)
})

addValToCombo()
renderChar('bar',2021)