# Graph of Neuroscientists

https://observablehq.com/d/585b2b94b29d2f4e@336

View this notebook in your browser by running a web server in this folder. For
example:

~~~sh
python3 -m http.server 9000
~~~

Or, use the [Observable Runtime](https://github.com/observablehq/runtime) to
import this module directly into your application. To npm install:

~~~sh
npm install @observablehq/runtime@4
npm install https://api.observablehq.com/d/585b2b94b29d2f4e.tgz?v=3
~~~

Then, import your notebook and the runtime as:

~~~js
import {Runtime, Inspector} from "@observablehq/runtime";
import define from "585b2b94b29d2f4e";
~~~

To log the value of the cell named “foo”:

~~~js
const runtime = new Runtime();
const main = runtime.module(define);
main.value("foo").then(value => console.log(value));
~~~
