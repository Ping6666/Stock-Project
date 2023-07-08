import axios from 'axios';

const axios_instance = axios.create({
    baseURL: `${window.location.protocol}//${window.location.host}/api`,
});

/* date */

const get_dates = async function () {
    const { data: { files, status } } = await axios_instance.get('/dates');
    return { status, files };
};

const get_date = async function (date_str) {
    const { data: { files, status } } = await axios_instance.get(`/date/${date_str}`);
    return { status, files };
};

const get_date_result = async function (date_str) {
    const { data: { files, status } } = await axios_instance.get(`/date/${date_str}/^^result.csv`);
    return { status, files };
};

/* symbol */

const get_symbols = async function () {
    const { data: { files, status } } = await axios_instance.get('/symbols');
    return { status, files };
};

const get_symbol = async function (symbol_str, download, overwrite) {
    const { data: res } = await axios_instance.get(
        `/symbol/${symbol_str}`,
        {
            params: {
                download: download,
                overwrite: overwrite,
            }
        },
    );
    return res;
};

export {
    get_dates,
    get_date,
    get_date_result,
    get_symbols,
    get_symbol,
};
