import event_sender, screen_fetcher, impls, resources

impl = impls.CommandLineTool()
print(impl.fetch("{}/test.png".format(resources.capture_output_path)))
# impl.click(0, 0)
