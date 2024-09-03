const dropdown_state = document.getElementById("state");
const dropdown_city = document.getElementById("city");

async function populateStates() {
    try {
        const response = await fetch("http://127.0.0.1:5000/getstates");       
        if (response.ok) {
            const stateList = await response.json();  // Correctly handle JSON response
            stateList.forEach(state => {
                // Create a new option element
                const option = document.createElement("option");

                // Set the value and text of the option
                option.value = state;
                option.text = state;

                // Add the option to the dropdown
                dropdown_state.appendChild(option);
            });
        } else {
            alert("HTTP-Error: " + response.status);
        }
    } catch (error) {
        console.error('Fetch error:', error);  // Handle any errors that occur during fetch
    }
}

async function populateCities(state) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/getcities/${state.value}`);       
        if (response.ok) {
            const cityList = await response.json();  // Correctly handle JSON response
            dropdown_city.innerHTML = "";
            cityList.forEach(city => {
                // Create a new option element
                const option = document.createElement("option");

                // Set the value and text of the option
                option.value = city;
                option.text = city;

                // Add the option to the dropdown
                dropdown_city.appendChild(option);
            });
        } else {
            alert("HTTP-Error: " + response.status);
        }
    } catch (error) {
        console.error('Fetch error:', error);  // Handle any errors that occur during fetch
    }
}

async function populatePlots(state, city) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/getdata/${state.value}/${city.value}`);       
        if (response.ok) {
            const dataJson = await response.json();  // Correctly handle JSON response
            const uniqueTypes = [...new Set(dataJson.map(item => item.type))];
            // Remove existing plot containers
            const existingPlots = document.querySelectorAll('.plot-container');
            existingPlots.forEach(plot => plot.remove());

            uniqueTypes.forEach((type, index) => {
                const filteredData = dataJson.filter(item => item.type === type);

                // Create a new div for each plot
                const plotContainer = document.createElement('div');
                plotContainer.className = 'plot-container';
                plotContainer.id = `plot${index + 1}`;  // Assign a unique id
                document.body.appendChild(plotContainer);  // Append to body or another container element

                const trace = {
                    x: filteredData.map(item => new Date(item.date)),
                    y: filteredData.map(item => item.value),
                    mode: 'lines+markers',
                    name: type,
                    type: 'scatter'
                };
                const layout = {
                    title: `Data for Type: ${type}`,
                    xaxis: { title: 'Date' },
                    yaxis: { title: 'Value' }
                };
                Plotly.newPlot(plotContainer.id, [trace], layout);
            });

        } else {
            alert("HTTP-Error: " + response.status);
        }
    } catch (error) {
        console.error('Fetch error:', error);  // Handle any errors that occur during fetch
    }
}

// Call the function to populate the dropdown
populateStates();