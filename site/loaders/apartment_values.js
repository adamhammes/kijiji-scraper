const path = require("path");
const fs = require("fs");

// To change which data is loaded, pass the --env.values_path option to webpack.
module.exports = content => {
  const defaultLocation = path.resolve(process.cwd(), "example_values.json");
  let jsonPath = defaultLocation;

  if (process.env.values_path) {
    jsonPath = process.env.values_path;
  } else if (process.env.KIJIJI_OUTPUT_DIRECTORY) {
    const potentialLocation = path.resolve(
      process.env.KIJIJI_OUTPUT_DIRECTORY,
      "trimmed_values.json"
    );
    if (fs.existsSync(potentialLocation)) {
      jsonPath = potentialLocation;
    }
  }

  const json = fs.readFileSync(jsonPath);
  return `module.exports = ${json}`;
};
