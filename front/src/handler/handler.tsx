import axios from "axios";

// Helper function to get CSRF token from cookie
function getCookie(name: string) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift();
}

const RecommendHandler = (input_val:string) => {
    const csrftoken = getCookie('csrftoken');
    console.log(csrftoken);
    // Include the CSRF token in the headers
    axios.defaults.headers.post['X-CSRFTOKEN'] = csrftoken;

    axios.post(
        ' http://127.0.0.1:8000/recommend',
        {
            'csrftoken': csrftoken,
            'input_val': input_val},
        {
            headers:{
                'content-type': 'application/json',
                'csrftoken': csrftoken,
            },
        }
        )
        .then(function(response) {
            // console.log(response);
        })
        .catch(function (error) {
            // console.log(error);
        });
}

export default RecommendHandler
