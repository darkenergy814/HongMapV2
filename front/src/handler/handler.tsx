import axios from "axios";

export const RecommendHandler = async (input_val: string): Promise<any> => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/recommend',
            JSON.stringify({ 'input_val': input_val }), {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return response.data['recommendations'];
    } catch (error) {
        console.error(error);
        return [];
    }
};

export const SubmitHandler = async (departure: string, destination: string): Promise<any> => {
    try {
        const response = await axios.post('http://127.0.0.1:8000/place_submit',
            JSON.stringify({ 'departure': departure, 'destination': destination }), {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
        console.log(response.data)
        return response.data;
    } catch (error) {
        console.error(error);
        return [];
    }
};
