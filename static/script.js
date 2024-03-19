$(document).ready(function() {
    // Function to fetch popular items from the server
    function fetchPopularItems() {
        $.ajax({
            url: '/popular_items', // URL of the route that returns popular items
            method: 'GET',
            success: function(response) {
                const shuffledItems = shuffle(response); // Shuffle the items array
                displayPopularItems(shuffledItems); // Call the function to display items
            },
            error: function(xhr, status, error) {
                console.error('Error fetching popular items:', error);
            }
        });
    }

    // Function to display popular items in the HTML
    function displayPopularItems(items) {
        const container = $('#popularItems');
        const row = $('<div class="row"></div>'); // Create a new row for each set of items

        items.forEach(item => {
            const htmlContent = `
                <div class="col-md-4 mb-4"> <!-- Use col-md-4 to display 3 items in a row on medium screens -->
                    <div class="card h-100">
                        <div class="card-img-container"> <!-- Container for image -->
                            <img src="${item.image}" class="card-img-top img-fluid" alt="${item.title}">
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">${item.title}</h5>
                            <p class="card-text">${item.description}</p>
                            <a href="/view/${item.id}" class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                </div>
            `;
            row.append(htmlContent); // Append each item's HTML content to the row
        });

        container.html(''); // Clear existing content
        container.append(row); // Append the row containing all items to the container
    }

    // Shuffle function to randomly shuffle the items array
    function shuffle(array) {
        let currentIndex = array.length, temporaryValue, randomIndex;

        // While there remain elements to shuffle...
        while (currentIndex !== 0) {

            // Pick a remaining element...
            randomIndex = Math.floor(Math.random() * currentIndex);
            currentIndex -= 1;

            // And swap it with the current element.
            temporaryValue = array[currentIndex];
            array[currentIndex] = array[randomIndex];
            array[randomIndex] = temporaryValue;
        }

        return array;
    }

    // Fetch popular items when the page loads
    fetchPopularItems();
});
