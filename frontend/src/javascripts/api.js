import axios from 'axios';

const axios_instance = axios.create({
    baseURL: `${window.location.protocol}//${window.location.host}/api`,
});

/* date */

const get_dates = async function () {
    const url = '/dates';

    let files = null;
    let status = null;

    try {
        const res = await axios_instance.get(url);

        status = res.data.status;
        files = res.data.files;
    } catch (err) {
        console.error(err);
    } finally {
        return { status, files };
    }
};

const get_date = async function (date_str) {
    const url = `/date/${date_str}`;

    let files = null;
    let status = null;

    try {
        const res = await axios_instance.get(url);

        status = res.data.status;
        files = res.data.files;
    } catch (err) {
        console.error(err);
    } finally {
        return { status, files };
    }
};

const get_date_result = async function (date_str) {
    const url = `/date/${date_str}/^^result.csv`;

    let files = null;
    let status = null;

    try {
        const res = await axios_instance.get(url);

        status = res.data.status;
        files = res.data.files;
    } catch (err) {
        console.error(err);
    } finally {
        return { status, files };
    }
};

const get_date_csv = async function (date_str, csv_str) {
    const url = `/date/${date_str}/${csv_str}`;

    let files = null;
    let status = null;

    try {
        const res = await axios_instance.get(url);

        status = res.data.status;
        files = res.data.files;
    } catch (err) {
        console.error(err);
    } finally {
        return { status, files };
    }
};

/* symbol */

const get_symbols = async function () {
    const url = '/symbols';

    let files = null;
    let status = null;

    try {
        const res = await axios_instance.get(url);

        status = res.data.status;
        files = res.data.files;
    } catch (err) {
        console.error(err);
    } finally {
        return { status, files };
    }
};

const get_symbol = async function (symbol_str, download, overwrite) {
    const url = `/symbol/${symbol_str}`;
    const config = {
        params: {
            download: download,
            overwrite: overwrite,
        }
    };

    let data = null;

    try {
        const res = await axios_instance.get(url, config);

        data = res.data;
    } catch (err) {
        console.error(err);
    } finally {
        return data;
    }
};

export {
    get_dates,
    get_date,
    get_date_result,
    get_date_csv,
    get_symbols,
    get_symbol,
};
