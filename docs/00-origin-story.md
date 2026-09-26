# Why this exists: the SupplierKit lesson

## The failure we are trying not to repeat

This framework comes from a concrete product failure.

While building **SupplierKit**, we received a great deal of encouraging customer feedback. People repeatedly told us the idea was good, the problem was real, the product would be useful, and the direction made sense. We accumulated what felt like near-constant validation.

The mistake was not that the feedback was false.

The mistake was treating **positive product anecdotes as evidence of demand**.

Those are different things.

A customer can:
- understand the problem;
- like the proposed solution;
- believe it would save time;
- tell you they would use it;
- ask for features;
- introduce you to colleagues;
- praise the product after seeing it;

and still never enter a viable buying motion.

That distinction became clear too late.

We built the product under the assumption that the positive response represented a sufficiently strong demand signal. What we had not validated early enough was the **buying shape** around that demand.

## What "buying shape" means here

The missing questions were closer to:

- When does this problem become an active Project rather than a recognized annoyance?
- What makes it Unavoidable now?
- What resources are already moving because the problem matters?
- What alternatives is the buyer actually using or evaluating?
- Why are those alternatives inadequate in this specific window?
- Who controls the resources required to solve the problem?
- Through what budget, approval, procurement, or substitution path can those resources move?
- What must a new option accomplish before the buyer will switch or commit?
- What observable action should occur next if the demand is real?

SupplierKit exposed a failure in the transaction path. The mechanism we expected would allow the product to be sold into the target budget did not work as we had assumed.

That failure mattered more than the volume of positive feedback.

## The bias hidden inside positive customer discovery

This creates an important lesson for qualitative research.

If a founder asks people whether a seemingly useful product would help them, the research process is already tilted toward collecting confirming evidence.

People are generally better at:
- recognizing potential usefulness;
- imagining benefits;
- agreeing with a familiar pain;
- suggesting improvements;

than they are at predicting whether they will overcome competing priorities, switching costs, internal approvals, procurement, implementation work, or budget constraints to actually acquire something.

An analysis system that simply ingests customer anecdotes and clusters the positive ones will therefore reproduce the founder's original bias at greater scale.

The agent must do the opposite.

It should preserve the positive evidence **and then actively search for the mechanism by which the apparent demand could fail**.

## What changed after SupplierKit

The SupplierKit experience led to a broader period of refining how demand is understood in both founder and product-leadership work.

Rob Snyder's PULL framework was useful because it shifted the object of analysis away from whether customers liked a product idea and toward the structure of a real customer Project:

- **Project**
- **Unavoidable**
- **List**
- **Limitations**

His later emphasis on starting with real **PULL anecdotes** rather than invented PULL hypotheses sharpened the lesson further: begin with observed behavior, not a persuasive market story.

This repository takes that foundation and adds an operational layer intended for product and founding teams working with large bodies of customer evidence.

## The design implication

The system should not answer:

> What demand hypothesis can we derive from these customer conversations?

It should answer:

> What appears to be happening in these customer conversations, what pattern might explain it, what evidence would make that pattern fail, and what do we need to observe next before treating it as a demand hypothesis?

That is why the core loop includes:
- negative cases;
- independent-case checks;
- selection-bias checks;
- rival explanations;
- transaction-path analysis;
- explicit falsification questions;
- an observable next commitment.

The purpose is not to eliminate uncertainty.

The purpose is to **spend uncertainty earlier**, while it is still cheap to discover that the team is wrong.

## The practical standard

A good analysis should make it harder for a team to say:

> "Customers love this, so we should build it."

and easier to say:

> "We have observed this Project repeatedly under these forcing conditions. These actors are already committing these resources. Their current options fail for these reasons. We believe a viable alternative must cross this acceptance boundary, and if we are right, we should see this specific buying-shaped action next. Here is the evidence that would cause us to abandon that belief."

That is the standard this repository is trying to operationalize.
