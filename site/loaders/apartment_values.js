const path = require('path');
const fs = require('fs');

// To change which data is loaded, pass the --env.values_path option to webpack.
module.exports = content => {
    const defaultLocation = path.resolve(process.cwd(), 'example_values.json');
    const jsonPath = process.env.values_path || defaultLocation;

    const json = fs.readFileSync(jsonPath)
    return `module.exports = ${json}`;
}
