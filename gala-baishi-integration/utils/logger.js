const levels = {
  debug: 0,
  info:  1,
  warn:  2,
  error: 3,
};

// Adjust this to change log verbosity: debug < info < warn < error
let currentLevel = levels.debug;

function format(level, message, ...args) {
  const timestamp = new Date().toISOString();
  return `[${timestamp}] [${level.toUpperCase()}] ${message}`;
}

export function setLogLevel(levelName) {
  if (levels[levelName] === undefined) {
    throw new Error(`Unknown log level: ${levelName}`);
  }
  currentLevel = levels[levelName];
}

export function debug(msg, ...args) {
  if (currentLevel <= levels.debug) {
    console.debug(format('debug', msg), ...args);
  }
}

export function info(msg, ...args) {
  if (currentLevel <= levels.info) {
    console.log(format('info', msg), ...args);
  }
}

export function warn(msg, ...args) {
  if (currentLevel <= levels.warn) {
    console.warn(format('warn', msg), ...args);
  }
}

export function error(msg, ...args) {
  if (currentLevel <= levels.error) {
    console.error(format('error', msg), ...args);
  }
}