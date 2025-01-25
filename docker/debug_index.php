<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

try {
    require_once realpath(dirname(__FILE__) . '/../const.php');
    require_once realpath(dirname(__FILE__) . '/../application/const.php');
    require_once _ROOT_DIR.DIRECTORY_SEPARATOR.'const.php';
    require_once _UTILS_PATH.'/Text.php';

    Utils_Text::checkMagicQuotes();

    header("Cache-Control: server");

    // Ensure library/ is on include_path
    set_include_path(implode(PATH_SEPARATOR, array(
        _LIBRARY_PATH,
        get_include_path(),
    )));

    /** Zend_Application */
    require_once 'Zend/Application.php';
      
    // Create application, bootstrap, and run
    $application = new Zend_Application(
      APPLICATION_ENV,
      _APPLICATION_CONFIG
    );

    $application->bootstrap()
                ->run();
} catch (Exception $e) {
    echo "<pre>";
    echo "Error: " . $e->getMessage() . "\n";
    echo "File: " . $e->getFile() . "\n";
    echo "Line: " . $e->getLine() . "\n";
    echo "Stack trace:\n" . $e->getTraceAsString() . "\n";
    echo "</pre>";
}
?>
